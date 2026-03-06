---
name: devforgeai-release
description: Orchestrate production releases with deployment automation, smoke testing, rollback capabilities, and release documentation. Use after QA approval to deploy stories to production. Supports multiple deployment strategies (blue-green, canary, rolling, recreate) and environments (staging, production). Enforces release gates and maintains deployment audit trail.
model: claude-opus-4-6
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

## Build Phase Enhancement (EPIC-036)

The release workflow includes optional build phases before deployment. These phases detect the project's technology stack and execute appropriate build commands.

**Configuration:** `devforgeai/deployment/build-config.yaml` (optional - defaults used if missing)

### Phase 0.1: Tech Stack Detection
**Purpose:** Automatically detect project's technology stack from indicator files
**Reference:** `references/tech-stack-detection.md`
**Detects:** Node.js, Python, .NET, Go, Rust, Java (Maven/Gradle)
**Output:** TechStackInfo with stack_type, build_command, output_directory

**Workflow:**
1. Load build-config.yaml (use defaults if missing)
2. If `build.enabled` = false, skip to Phase 1
3. Scan for indicator files (package.json, pyproject.toml, *.csproj, etc.)
4. Return TechStackInfo for each detected stack
5. Pass results to Phase 0.2

### Phase 0.2: Build/Compile
**Purpose:** Execute build commands for detected technology stacks
**Reference:** `references/build-commands.md`
**Commands:** npm run build, dotnet publish, python -m build, cargo build, etc.
**Output:** BuildResult with success, output_path, duration_ms, stdout, stderr

**Workflow:**
1. For each TechStackInfo from Phase 0.1:
   - Execute build command with configured timeout
   - Capture stdout/stderr
   - Record success/failure
2. Aggregate BuildResult objects
3. If `build.fail_on_build_error` = true and any build failed: HALT
4. Pass BuildResult list to Phase 1 (Pre-Release Validation)

**Build Results Available to Subsequent Phases:**
The BuildResult objects from Phase 0.2 are available to Phase 1 for validation:
- `build_results[]` - Array of BuildResult objects
- Each contains: success, stack_type, output_path, duration_ms

---

## Release Workflow (10 Phases)

**⚠️ EXECUTION STARTS HERE - You are now executing the skill's workflow.**

Each phase loads its reference file on-demand for detailed implementation.

**Build Phases (0.x):** Tech stack detection and build execution (optional, enabled by default)

### Phase 0.3: Project Type Classification (STORY-498)

**Purpose:** Detect project type and set phase applicability for adaptive release paths

**Reference:** RCA-041 (Release Skill Phase Skip Violation)

**Workflow:**

1. Read the project's build configuration file using Read() tool (no Bash parsing)
2. Classify project as one of: "library", "cli", or "api"
3. Set SKIP_PHASES and ACTIVE_PHASES based on classification
4. Display detected type and phase plan to user
5. Proceed to Phase 0.5 (or Phase 1 if 0.5 skipped)

**Detection Matrix:**

| Ecosystem | Config File | Library Signal | CLI Signal | API Signal |
|-----------|------------|----------------|------------|------------|
| Rust | `Cargo.toml` | `[lib]` without `[[bin]]` and no `src/main.rs` | Has `[[bin]]` target | HTTP server dependency (actix-web, rocket, axum) |
| Node.js | `package.json` | No `bin` field, no server deps | Has `bin` field | Has express, fastify, koa, or hapi dependency |
| Python | `pyproject.toml` | No `[project.scripts]`, no server deps | Has `[project.scripts]` entry | Has uvicorn, gunicorn, or flask dependency |

**Classification Logic:**

```
# Step 1: Detect ecosystem from build config
config_files = Glob(pattern="Cargo.toml") OR Glob(pattern="package.json") OR Glob(pattern="pyproject.toml")

IF no config file found:
    HALT: "No recognized build configuration found"
    AskUserQuestion: "What is the project type?"
    Options: ["library", "cli", "api"]

# Step 2: Read config and classify
Read(file_path=config_file)

# Rust classification
IF Cargo.toml:
    IF has [lib] AND NOT has [[bin]] AND NOT exists src/main.rs → "library"
    ELIF has [[bin]] → "cli"
    ELIF has actix-web OR rocket OR axum dependency → "api"
    ELSE → AskUserQuestion (ambiguous)

# Node.js classification
IF package.json:
    IF NOT has "bin" field AND NOT has express/fastify/koa → "library"
    ELIF has "bin" field → "cli"
    ELIF has express OR fastify OR koa OR hapi → "api"
    ELSE → AskUserQuestion (ambiguous)

# Python classification
IF pyproject.toml:
    IF NOT has [project.scripts] AND NOT has uvicorn/gunicorn → "library"
    ELIF has [project.scripts] → "cli"
    ELIF has uvicorn OR gunicorn OR flask → "api"
    ELSE → AskUserQuestion (ambiguous)
```

**Phase Applicability by Project Type:**

| Project Type | SKIP_PHASES | ACTIVE_PHASES | Rationale |
|-------------|-------------|---------------|-----------|
| **library** | [2, 2.5, 3, 3.5, 4, 6] | [1, 5, 7] | Library project: no deployment target |
| **cli** | [] | [1, 2, 2.5, 3, 3.5, 4, 5, 6, 7] | CLI has deployable binary |
| **api** | [] | [1, 2, 2.5, 3, 3.5, 4, 5, 6, 7] | API has deployable service |

```
IF project_type == "library":
    SKIP_PHASES = [2, 2.5, 3, 3.5, 4, 6]
    ACTIVE_PHASES = [1, 5, 7]
ELIF project_type == "cli" OR project_type == "api":
    SKIP_PHASES = []
    ACTIVE_PHASES = [1, 2, 2.5, 3, 3.5, 4, 5, 6, 7]
```

**Skipped Phase Handling (per STORY-497 marker protocol):**

For each phase in SKIP_PHASES:
1. Load reference file for the phase (mandatory — even skipped phases load references)
2. Write a skip marker with documented reason:
```
Write(file_path="devforgeai/workflows/.release-phase-{N}.marker",
      content="phase: {N}\nstory_id: ${STORY_ID}\nstatus: skipped\nreason: Library project: no deployment target\ntimestamp: ${ISO_8601}")
```
3. Advance to the next phase in execution order without executing deployment logic

**Display: Phase Plan Output**

After classification completes, display the detected project type and phase status table:

```
Display:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 0.3: Project Type: ${PROJECT_TYPE}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Phase | Name                        | Status  |
|-------|-----------------------------|---------|
| 1     | Pre-Release Validation      | Active  |
| 2     | Staging Deployment          | Active/Skipped |
| 2.5   | Post-Staging Hooks          | Active/Skipped |
| 3     | Production Deployment       | Active/Skipped |
| 3.5   | Post-Production Hooks       | Active/Skipped |
| 4     | Post-Deployment Validation  | Active/Skipped |
| 5     | Release Documentation       | Active  |
| 6     | Post-Release Monitoring     | Active/Skipped |
| 7     | Session Checkpoint Cleanup  | Active  |
```

**Ambiguity Fallback:**

IF detection cannot determine project type (missing config, workspace/monorepo, unrecognized ecosystem):
```
AskUserQuestion:
  Question: "Unable to determine project type automatically. What type is this project?"
  Header: "Project Type"
  Options:
    - "library (no deployment target, publish only)"
    - "cli (deployable binary/executable)"
    - "api (deployable HTTP service)"
  multiSelect: false
```

---

### Phase 0.5: Registry Publishing (Optional) - EPIC-038

**Purpose:** Publish packages to configured registries before deployment

**Skip with:** `--skip-registry` flag | **Dry-run:** `--dry-run` flag validates without publishing

**Reference:** See `references/registry-publishing.md` for detailed commands and credentials

**Workflow:**
1. Load `devforgeai/deployment/registry-config.yaml` (skip if missing)
2. Validate credentials for enabled registries
3. Publish to each registry in sequence (npm, PyPI, NuGet, Docker, GitHub, crates.io)
4. Aggregate results and display per-registry status

**Failure Handling:** If any registry fails, prompt user:
- "Registry publish failed: {registries}. Continue to deployment? [Y/n]"
- Continue: Proceed with warning logged to story change log
- Abort: Halt release workflow

**Output Format:**
```
[npm]    ✓ Published package@1.0.0
[pypi]   ✓ Published package-1.0.0
[docker] ✗ Failed: authentication error (retry 2/3)
```

### Phase 1: Pre-Release Validation

**Phase 1 Pre-Flight: Clean Starting State (AC#5 - STORY-497)**

```
# Check for stale markers from previous release runs
Glob(pattern="devforgeai/workflows/.release-phase-*.marker")

IF stale markers found:
    Display: "⚠️ Found {count} stale release markers from a previous run."
    AskUserQuestion: "Stale release markers detected. Clean up before proceeding?"
    Options: ["Yes, delete stale markers and proceed", "No, abort release"]

    IF user selects cleanup:
        # Delete each stale marker
        FOR marker in stale_markers:
            Bash(command="rm {marker}")
        Display: "✓ Stale markers cleaned up"
    ELSE:
        HALT: "Release aborted - stale markers not cleaned"
```

### ⚠️ CHECKPOINT: MANDATORY - Phase 1 Reference Loading

```
Read(file_path=".claude/skills/devforgeai-release/references/pre-release-validation.md")
```

**Purpose:** Validate all prerequisites before deployment
**Reference:** `pre-release-validation.md`
**Checklist:** `release-checklist.md`
**Validates:** QA approval, tests passing, build success, config exists, dependencies released
**Output:** Validation status (PASS/FAIL with details)

### Phase 1 Marker Write

```
Write(file_path="devforgeai/workflows/.release-phase-1.marker",
      content="phase: 1\nstory_id: ${STORY_ID}\nstatus: complete\nreason: Pre-release validation completed successfully\ntimestamp: ${ISO_8601}")
```

### Phase 2: Staging Deployment

**Pre-Flight: Verify Phase 1 Complete**

```
Glob(pattern="devforgeai/workflows/.release-phase-1.marker")

IF marker file NOT found:
    HALT: "Phase 2 cannot start: Phase 1 missing marker. Prerequisite phase must complete before proceeding."
```

### ⚠️ CHECKPOINT: MANDATORY - Phase 2 Reference Loading

```
Read(file_path=".claude/skills/devforgeai-release/references/staging-deployment.md")
```

**Purpose:** Deploy to staging environment and run smoke tests
**Reference:** `staging-deployment.md`
**Guides:** `deployment-strategies.md`, `platform-deployment-commands.md`, `smoke-testing-guide.md`
**Steps:** Deploy → Smoke test → Health check → Validate
**Output:** Staging deployment complete, smoke tests passed

**IF phase is not applicable (no staging environment configured):**
```
Read(file_path=".claude/skills/devforgeai-release/references/staging-deployment.md")
Write(file_path="devforgeai/workflows/.release-phase-2.marker",
      content="phase: 2\nstory_id: ${STORY_ID}\nstatus: skipped\nreason: Phase not applicable - no staging environment configured\ntimestamp: ${ISO_8601}")
```

### Phase 2 Marker Write

```
Write(file_path="devforgeai/workflows/.release-phase-2.marker",
      content="phase: 2\nstory_id: ${STORY_ID}\nstatus: complete\nreason: Staging deployment completed successfully\ntimestamp: ${ISO_8601}")
```

### Phase 2.5: Post-Staging Hooks (NEW - STORY-025)
**Purpose:** Trigger retrospective feedback after staging deployment
**Reference:** `post-staging-hooks.md`
**Invokes:** `devforgeai-validate check-hooks --operation=release-staging --status=$STATUS`
**Conditional:** Only invokes `devforgeai-validate invoke-hooks` if check-hooks returns 0 (eligible)
**Graceful Degradation:** Hook failures logged, deployment proceeds regardless
**Output:** Feedback collected (if hooks enabled), deployment continues

### Phase 3: Production Deployment

**Pre-Flight: Verify Phase 2 Complete**

```
Glob(pattern="devforgeai/workflows/.release-phase-2.marker")

IF marker file NOT found:
    HALT: "Phase 3 cannot start: Phase 2 missing marker. Prerequisite phase must complete before proceeding."
```

### ⚠️ CHECKPOINT: MANDATORY - Phase 3 Reference Loading

```
Read(file_path=".claude/skills/devforgeai-release/references/production-deployment.md")
```

**Purpose:** Deploy to production with progressive rollout
**Reference:** `production-deployment.md`
**Guides:** `deployment-strategies.md`, `platform-deployment-commands.md`
**Strategies:** Blue-green (zero downtime), canary (progressive), rolling (gradual), recreate (simple)
**Output:** Production deployment complete with chosen strategy

### Phase 3 Marker Write

```
Write(file_path="devforgeai/workflows/.release-phase-3.marker",
      content="phase: 3\nstory_id: ${STORY_ID}\nstatus: complete\nreason: Production deployment completed successfully\ntimestamp: ${ISO_8601}")
```

### Phase 3.5: Post-Production Hooks (NEW - STORY-025)
**Purpose:** Trigger retrospective feedback after production deployment
**Reference:** `post-production-hooks.md`
**Invokes:** `devforgeai-validate check-hooks --operation=release-production --status=$STATUS`
**Conditional:** Only invokes `devforgeai-validate invoke-hooks` if check-hooks returns 0 (eligible)
**Default Behavior:** Failures-only mode (skips feedback on production success unless configured)
**Graceful Degradation:** Hook failures logged, deployment proceeds regardless
**Output:** Feedback collected (if hooks enabled and eligible), deployment continues

### Phase 4: Parallel Post-Deployment Validation (UPDATED - STORY-113)

**Pre-Flight: Verify Phase 3 Complete**

```
Glob(pattern="devforgeai/workflows/.release-phase-3.marker")

IF marker file NOT found:
    HALT: "Phase 4 cannot start: Phase 3 missing marker. Prerequisite phase must complete before proceeding."
```

### ⚠️ CHECKPOINT: MANDATORY - Phase 4 Reference Loading

```
Read(file_path=".claude/skills/devforgeai-release/references/parallel-smoke-tests.md")
```

**⚠️ You MUST execute health checks AND smoke tests in PARALLEL (same batch)**

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

### Phase 4 Marker Write

```
Write(file_path="devforgeai/workflows/.release-phase-4.marker",
      content="phase: 4\nstory_id: ${STORY_ID}\nstatus: complete\nreason: Post-deployment validation completed successfully\ntimestamp: ${ISO_8601}")
```

### Phase 5: Release Documentation and Story Archival

**Pre-Flight: Verify Phase 4 Complete**

```
Glob(pattern="devforgeai/workflows/.release-phase-4.marker")

IF marker file NOT found:
    HALT: "Phase 5 cannot start: Phase 4 missing marker. Prerequisite phase must complete before proceeding."
```

### ⚠️ CHECKPOINT: MANDATORY - Phase 5 Reference Loading

```
Read(file_path=".claude/skills/devforgeai-release/references/release-documentation.md")
```

**Purpose:** Generate release notes, update story, archive to Stories/archive/, update CHANGELOG.md
**Reference:** `release-documentation.md`, `.claude/references/changelog-update-guide.md`

**Step 5.1: Generate Release Notes**
See `release-documentation.md` Step 1 for template.

**Step 5.2: Append Change Log Entry**
Author: `.claude/deployment-engineer`
Phase/Action: `Released`
Change: Description (e.g., "Deployed v1.2.3 to production")

```
Edit(
    file_path="devforgeai/specs/Stories/{STORY-ID}.story.md",
    old_string="| {last_entry} |",
    new_string="| {last_entry} |\n| {timestamp} | .claude/deployment-engineer | Released | Deployed {version} to production | CHANGELOG.md |"
)

# Update Current Status to Released
Edit(
    file_path="devforgeai/specs/Stories/{STORY-ID}.story.md",
    old_string="**Current Status:** QA Approved",
    new_string="**Current Status:** Released"
)
```

**Step 5.3: Update CHANGELOG.md (Keep a Changelog format)**

If CHANGELOG.md exists, add entry under `## [Unreleased]`:
```
Edit(file_path="CHANGELOG.md",
     old_string="## [Unreleased]",
     new_string="## [Unreleased]\n\n- {story_title} ([{STORY_ID}])")

# Add reference link at bottom
Append: "[{STORY_ID}]: devforgeai/specs/Stories/archive/{STORY_ID}.story.md"
```

**Step 5.4: Archive Story File**
Move story to archive directory:
```
Bash(command="mv devforgeai/specs/Stories/{STORY_ID}.story.md devforgeai/specs/Stories/archive/")
```

**Updates:** Story status = "Released", changelog entry, CHANGELOG.md, story archived
**Output:** Documentation complete, audit trail created

### Phase 5 Marker Write

```
Write(file_path="devforgeai/workflows/.release-phase-5.marker",
      content="phase: 5\nstory_id: ${STORY_ID}\nstatus: complete\nreason: Release documentation completed successfully\ntimestamp: ${ISO_8601}")
```

### Phase 6: Post-Release Monitoring & Closure

**Pre-Flight: Verify Phase 5 Complete**

```
Glob(pattern="devforgeai/workflows/.release-phase-5.marker")

IF marker file NOT found:
    HALT: "Phase 6 cannot start: Phase 5 missing marker. Prerequisite phase must complete before proceeding."
```

### ⚠️ CHECKPOINT: MANDATORY - Phase 6 Reference Loading

```
Read(file_path=".claude/skills/devforgeai-release/references/monitoring-closure.md")
```

**Purpose:** Set up monitoring and close story
**Reference:** `monitoring-closure.md`
**Guide:** `monitoring-metrics.md`
**Setup:** Error tracking, performance monitoring, alerting rules
**Output:** Monitoring configured, story closed

### Phase 6 Marker Write

```
Write(file_path="devforgeai/workflows/.release-phase-6.marker",
      content="phase: 6\nstory_id: ${STORY_ID}\nstatus: complete\nreason: Post-release monitoring configured successfully\ntimestamp: ${ISO_8601}")
```

### Phase 7: Session Checkpoint Cleanup (AC#4 - STORY-120)

**Pre-Flight: Verify Phase 6 Complete**

```
Glob(pattern="devforgeai/workflows/.release-phase-6.marker")

IF marker file NOT found:
    HALT: "Phase 7 cannot start: Phase 6 missing marker. Prerequisite phase must complete before proceeding."
```

### ⚠️ CHECKPOINT: MANDATORY - Phase 7 Reference Loading
```
Read(file_path=".claude/skills/devforgeai-release/references/monitoring-closure.md")
```

**Purpose:** Clean up session checkpoint after story reaches Released status
**Trigger:** After story status = "Released"

```
Bash(command="python3 -c '
from devforgeai_cli.session.checkpoint import delete_checkpoint
if delete_checkpoint(\"$STORY_ID\"):
    print(\"✓ Session checkpoint cleaned up\")
else:
    print(\"ℹ No checkpoint to clean up\")
'")
```

**Rationale:** Checkpoints are only needed for resuming in-progress development. Once Released, checkpoint is no longer needed and should be cleaned up to prevent storage bloat.

**IF phase is not applicable (no checkpoint exists):**
```
Write(file_path="devforgeai/workflows/.release-phase-7.marker",
      content="phase: 7\nstory_id: ${STORY_ID}\nstatus: skipped\nreason: Phase not applicable - no session checkpoint to clean up\ntimestamp: ${ISO_8601}")
```

### Phase 7 Marker Write

```
Write(file_path="devforgeai/workflows/.release-phase-7.marker",
      content="phase: 7\nstory_id: ${STORY_ID}\nstatus: complete\nreason: Session checkpoint cleanup completed successfully\ntimestamp: ${ISO_8601}")
```

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

### Workflow Files (15 files)
- **parameter-extraction.md** (104 lines) - Story ID, environment, strategy extraction algorithm
- **configuration-guide.md** (52 lines) - Platform config requirements, schemas, examples
- **tech-stack-detection.md** (NEW - STORY-238) - Phase 0.1: Technology stack auto-detection
- **build-commands.md** (NEW - STORY-240) - Phase 0.2: Build command execution templates
- **package-formats.md** (NEW - STORY-241) - Phase 0.3: Language-specific package creation
- **registry-publishing.md** (NEW - STORY-246) - Phase 0.5: Registry publishing commands and credentials
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

**Total: 20 reference files, ~5,400 lines of comprehensive deployment guidance.**
- 14 workflow files (phases 0.1-0.3 + phase 0.5 + phases 1-6 + 2 hook phases + 1 parallel pattern)
- 6 guide files (strategies, monitoring, platforms, checklists, rollback, smoke testing)

**Progressive loading ensures only needed references consume tokens during execution.**

**Hook Integration (STORY-025):**
- Phase 2.5 and 3.5 add retrospective feedback collection
- Non-blocking: Hook failures never affect deployment status
- Configurable: `devforgeai/config/hooks.yaml` controls behavior
- See: `post-staging-hooks.md` and `post-production-hooks.md` for implementation details
