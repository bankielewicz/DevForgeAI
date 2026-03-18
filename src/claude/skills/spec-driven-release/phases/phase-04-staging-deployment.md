# Phase 04: Staging Deployment

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --workflow=release --from=03 --to=04 --project-root=.
```

## Contract

PURPOSE: Deploy to staging environment, run smoke tests, execute post-staging hooks for feedback collection.
REQUIRED SUBAGENTS: deployment-engineer (BLOCKING)
REQUIRED ARTIFACTS: Staging deployment status, smoke test results, hook invocation status
STEP COUNT: 8 mandatory steps

---

## Mandatory Steps

### Step 4.1: Check Phase Applicability

EXECUTE: Check if this phase should be skipped for library projects.
```
IF 04 in $SKIP_PHASES:
    Read(file_path=".claude/skills/spec-driven-release/references/staging-deployment.md")
    # Reference loaded even for skipped phases (mandatory)

    Write(file_path="devforgeai/workflows/.release-phase-04.marker",
          content="phase: 04\nstory_id: ${STORY_ID}\nstatus: skipped\nreason: Library project - no staging deployment target\ntimestamp: ${ISO_8601}")

    Display: "Phase 04 skipped: Library project - no staging deployment target"
    EXIT phase early (proceed to Exit Gate with skip status)

Display: "Phase 04 active - proceeding with staging deployment"
```
VERIFY: Either phase is active (proceed) OR skip marker written and phase exits early.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=04 --step=4.1 --project-root=.`

---

### Step 4.2: Load Staging Deployment References

EXECUTE: Load all references needed for staging deployment.
```
Read(file_path=".claude/skills/spec-driven-release/references/staging-deployment.md")
Read(file_path=".claude/skills/spec-driven-release/references/platform-deployment-commands.md")
Read(file_path=".claude/skills/spec-driven-release/references/smoke-testing-guide.md")
```
VERIFY: All three reference files loaded successfully.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=04 --step=4.2 --project-root=.`

---

### Step 4.3: Prepare Deployment Artifacts

EXECUTE: Prepare artifacts for staging deployment.
```
# Create git tag for release
Bash(command="git tag -a v${VERSION}-staging -m 'Staging release for ${STORY_ID}'")

# Verify build artifacts from Phase 02 are available
IF $BUILD_RESULTS:
    FOR each result in $BUILD_RESULTS:
        IF result.success:
            Glob(pattern="${result.output_path}/*")
            IF artifacts found:
                Display: "Build artifacts available: ${result.output_path}"
            ELSE:
                HALT: "Build artifacts missing at ${result.output_path}. Re-run Phase 02."

# Prepare deployment manifest from template if needed
Glob(pattern="devforgeai/deployment/*staging*")
IF staging config found:
    Read(file_path=staging_config)
    Display: "Staging deployment config loaded"
ELSE:
    Display: "Using default staging configuration"
```
VERIFY: Git tag created AND build artifacts available (or no build required).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=04 --step=4.3 --project-root=.`

---

### Step 4.4: Invoke Deployment-Engineer Subagent

EXECUTE: Launch deployment-engineer subagent (BLOCKING) for staging deployment.
```
Agent(subagent_type="deployment-engineer",
      prompt="Deploy ${STORY_ID} to STAGING environment.
              Strategy: ${DEPLOYMENT_STRATEGY}
              Tech Stack: ${TECH_STACK_INFO.stack_type}
              Build Output: ${BUILD_RESULTS[0].output_path}

              Execute staging deployment following the platform-specific deployment commands.
              Report: deployment status, endpoints, version deployed, any warnings.")

$STAGING_DEPLOY_RESULT = {
    success: agent_result.success,
    endpoints: agent_result.endpoints,
    version: agent_result.version,
    warnings: agent_result.warnings
}

IF NOT $STAGING_DEPLOY_RESULT.success:
    HALT: "Staging deployment failed. Check deployment-engineer output for details."

Display: "Staging deployment: SUCCESS"
Display: "Endpoints: ${STAGING_DEPLOY_RESULT.endpoints}"
```
VERIFY: $STAGING_DEPLOY_RESULT.success = true. If false, workflow HALTED.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=04 --step=4.4 --project-root=.`

---

### Step 4.5: Execute Staging Health Checks

EXECUTE: Run health checks against staging endpoints.
```
FOR each endpoint in $STAGING_DEPLOY_RESULT.endpoints:
    Bash(command="python .claude/skills/spec-driven-release/scripts/health_check.py --url=${endpoint} --timeout=30")

    IF exit_code != 0:
        Display: "Health check FAILED: ${endpoint}"
        $HEALTH_CHECK_FAILURES[] = endpoint
    ELSE:
        Display: "Health check PASSED: ${endpoint} (HTTP 200)"

IF $HEALTH_CHECK_FAILURES.length > 0:
    Display: "Warning: ${HEALTH_CHECK_FAILURES.length} health check(s) failed"
    AskUserQuestion:
        Question: "Health checks failed for: ${HEALTH_CHECK_FAILURES.join(', ')}. Continue or abort?"
        Header: "Health"
        Options:
            - label: "Continue with smoke tests"
              description: "Proceed to smoke tests despite health check failures"
            - label: "Abort and rollback staging"
              description: "Stop deployment and revert staging"
        multiSelect: false

    IF user selects abort:
        Read(file_path=".claude/skills/spec-driven-release/references/rollback-procedures.md")
        HALT: "Staging deployment rolled back due to health check failures"
```
VERIFY: Either all health checks passed OR user acknowledged failures and chose to continue.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=04 --step=4.5 --project-root=.`

---

### Step 4.6: Execute Staging Smoke Tests

EXECUTE: Run smoke test suite against staging environment.
```
Bash(command="python .claude/skills/spec-driven-release/scripts/smoke_test_runner.py --env=staging --config=devforgeai/smoke-tests/config.json", timeout=180000)

IF exit_code != 0:
    Display: "Smoke tests FAILED on staging"
    Display: "stdout: ${stdout}"
    AskUserQuestion:
        Question: "Staging smoke tests failed. How to proceed?"
        Header: "Smoke Tests"
        Options:
            - label: "Investigate and retry"
              description: "Review failures before deciding"
            - label: "Proceed to production anyway"
              description: "Accept risk and continue (not recommended)"
            - label: "Abort release"
              description: "Stop release workflow"
        multiSelect: false

    IF user selects abort:
        HALT: "Release aborted - staging smoke tests failed"
ELSE:
    Display: "Staging smoke tests: PASSED"
```
VERIFY: Smoke tests passed OR user chose to proceed despite failures.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=04 --step=4.6 --project-root=.`

---

### Step 4.7: Optional Manual Validation

EXECUTE: Ask user if staging looks good before proceeding.
```
AskUserQuestion:
    Question: "Staging deployment complete for ${STORY_ID}. Ready to proceed to production?"
    Header: "Staging OK"
    Options:
        - label: "Proceed to production"
          description: "Staging validated - continue to production deployment"
        - label: "Investigate staging"
          description: "Need more time to validate staging environment"
        - label: "Abort release"
          description: "Stop release workflow"
    multiSelect: false

IF user selects abort:
    HALT: "Release aborted by user after staging validation"
ELIF user selects investigate:
    Display: "Pausing for manual investigation. Re-run /release ${STORY_ID} when ready."
    HALT: "Release paused for manual staging investigation"

Display: "User confirmed staging is ready"
```
VERIFY: User confirmed staging is acceptable and chose to proceed.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=04 --step=4.7 --project-root=.`

---

### Step 4.8: Invoke Post-Staging Hooks

EXECUTE: Trigger retrospective feedback hooks after staging deployment. Non-blocking.
```
Read(file_path=".claude/skills/spec-driven-release/references/post-staging-hooks.md")

$STAGING_STATUS = $STAGING_DEPLOY_RESULT.success ? "SUCCESS" : "FAILURE"

Bash(command="devforgeai-validate check-hooks --operation=release-staging --status=${STAGING_STATUS} 2>&1")

IF exit_code == 0:
    Display: "Post-staging hooks eligible - invoking..."
    Bash(command="devforgeai-validate invoke-hooks --operation=release-staging --context='environment=staging,deployment_status=${STAGING_STATUS},story_id=${STORY_ID}' 2>&1")
    Display: "Post-staging hooks invoked (non-blocking)"
ELSE:
    Display: "Post-staging hooks: not eligible or not configured (skipped)"

# Non-blocking: hook failures do NOT affect deployment
```
VERIFY: Hook check completed (exit code recorded). Hook invocation attempted if eligible. Failures logged but not blocking.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=04 --step=4.8 --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --workflow=release --phase=04 --checkpoint-passed --project-root=.
```

## Phase 04 Completion Display

```
Phase 04 Complete: Staging Deployment
  Deployment: ${STAGING_DEPLOY_RESULT.success ? 'SUCCESS' : 'SKIPPED'}
  Health Checks: ${health_passed}/${health_total} passed
  Smoke Tests: PASSED
  Post-Staging Hooks: ${hooks_invoked ? 'Invoked' : 'Skipped'}
  User Validation: Confirmed
```
