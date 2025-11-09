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

**Prerequisites:** QA approved, tests passing, build successful, config exists in `.devforgeai/deployment/`

**Invoked by:**
- `/release` command (user-initiated)
- devforgeai-orchestration skill (automated progression)

---

## Configuration

Platform configs required in `.devforgeai/deployment/` (K8s, Docker, AWS, Azure, GCP, Vercel, Netlify, VPS)

Smoke tests config in `.devforgeai/smoke-tests/config.json` (URLs, test users, API keys)

**See `references/configuration-guide.md` for schemas and examples.**

---

## Release Workflow (6 Phases)

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

### Phase 3: Production Deployment
**Purpose:** Deploy to production with progressive rollout
**Reference:** `production-deployment.md`
**Guides:** `deployment-strategies.md`, `platform-deployment-commands.md`
**Strategies:** Blue-green (zero downtime), canary (progressive), rolling (gradual), recreate (simple)
**Output:** Production deployment complete with chosen strategy

### Phase 4: Post-Deployment Validation
**Purpose:** Execute comprehensive smoke tests on production
**Reference:** `post-deployment-validation.md`
**Guide:** `smoke-testing-guide.md`, `monitoring-metrics.md`
**Tests:** Health checks (endpoints alive), critical path (core workflows), performance (latency within bounds)
**Output:** Production validation complete (all tests passed)

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

### Workflow Files (8 files - NEW)
- **parameter-extraction.md** (104 lines) - Story ID, environment, strategy extraction algorithm
- **configuration-guide.md** (52 lines) - Platform config requirements, schemas, examples
- **pre-release-validation.md** (66 lines) - Phase 1: Validation checks and release gates
- **staging-deployment.md** (75 lines) - Phase 2: Staging workflow and smoke testing
- **production-deployment.md** (69 lines) - Phase 3: Production deployment with strategies
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

**Total: 14 reference files, 3,601 lines of comprehensive deployment guidance.**

**Progressive loading ensures only needed references consume tokens during execution.**
