# Phase 05: Production Deployment

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --workflow=release --from=04 --to=05 --project-root=.
```

## Contract

PURPOSE: Deploy to production with security audit, progressive rollout, health checks, and post-production hooks.
REQUIRED SUBAGENTS: deployment-engineer (BLOCKING), security-auditor (BLOCKING)
REQUIRED ARTIFACTS: Production deployment status, security audit results, hook invocation status
STEP COUNT: 8 mandatory steps

---

## Mandatory Steps

### Step 5.1: Check Phase Applicability

EXECUTE: Check if this phase should be skipped for library projects.
```
IF 05 in $SKIP_PHASES:
    Read(file_path=".claude/skills/spec-driven-release/references/production-deployment.md")
    # Reference loaded even for skipped phases (mandatory)

    Write(file_path="devforgeai/workflows/.release-phase-05.marker",
          content="phase: 05\nstory_id: ${STORY_ID}\nstatus: skipped\nreason: Library project - no production deployment target\ntimestamp: ${ISO_8601}")

    Display: "Phase 05 skipped: Library project - no production deployment target"
    EXIT phase early (proceed to Exit Gate with skip status)

Display: "Phase 05 active - proceeding with production deployment"
```
VERIFY: Either phase is active (proceed) OR skip marker written and phase exits early.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=05 --step=5.1 --project-root=.`

---

### Step 5.2: Load Production Deployment References

EXECUTE: Load all references needed for production deployment.
```
Read(file_path=".claude/skills/spec-driven-release/references/production-deployment.md")
Read(file_path=".claude/skills/spec-driven-release/references/deployment-strategies.md")
Read(file_path=".claude/skills/spec-driven-release/references/platform-deployment-commands.md")
```
VERIFY: All three reference files loaded successfully.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=05 --step=5.2 --project-root=.`

---

### Step 5.3: Invoke Security-Auditor Pre-Production

EXECUTE: Launch security-auditor subagent (BLOCKING) for pre-production security scan.
```
Agent(subagent_type="security-auditor",
      prompt="Pre-production security audit for ${STORY_ID}.
              Run: OWASP Top 10 checks, dependency vulnerability scan, hardcoded secrets detection, auth/authz review.
              Report: severity (CRITICAL/HIGH/MEDIUM/LOW), findings, recommendations.")

$SECURITY_RESULTS = {
    critical_count: agent_result.critical,
    high_count: agent_result.high,
    findings: agent_result.findings
}

IF $SECURITY_RESULTS.critical_count > 0:
    Display: "CRITICAL security findings: ${SECURITY_RESULTS.critical_count}"
    FOR each finding in critical_findings:
        Display: "  CRITICAL: ${finding.description}"
    HALT: "Production deployment blocked: CRITICAL security findings. Fix before deploying."

IF $SECURITY_RESULTS.high_count > 0:
    Display: "HIGH security findings: ${SECURITY_RESULTS.high_count}"
    AskUserQuestion:
        Question: "Security audit found ${SECURITY_RESULTS.high_count} HIGH findings. Deploy to production anyway?"
        Header: "Security"
        Options:
            - label: "Proceed with HIGH findings"
              description: "Accept risk and deploy (findings logged)"
            - label: "Abort to fix findings"
              description: "Stop release to address security issues"
        multiSelect: false

    IF user selects abort:
        HALT: "Release aborted - HIGH security findings"

Display: "Security audit: PASSED (${SECURITY_RESULTS.critical_count} critical, ${SECURITY_RESULTS.high_count} high)"
```
VERIFY: Zero CRITICAL findings. HIGH findings either zero OR user acknowledged.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=05 --step=5.3 --project-root=.`

---

### Step 5.4: Invoke Deployment-Engineer for Production

EXECUTE: Launch deployment-engineer subagent (BLOCKING) for production deployment.
```
Agent(subagent_type="deployment-engineer",
      prompt="Deploy ${STORY_ID} to PRODUCTION environment.
              Strategy: ${DEPLOYMENT_STRATEGY}
              Tech Stack: ${TECH_STACK_INFO.stack_type}
              Build Output: ${BUILD_RESULTS[0].output_path}

              Execute production deployment using ${DEPLOYMENT_STRATEGY} strategy.
              Report: deployment status, endpoints, version deployed, rollback command.")

$PRODUCTION_DEPLOY_RESULT = {
    success: agent_result.success,
    endpoints: agent_result.endpoints,
    version: agent_result.version,
    rollback_command: agent_result.rollback_command
}

IF NOT $PRODUCTION_DEPLOY_RESULT.success:
    Display: "Production deployment FAILED"
    Read(file_path=".claude/skills/spec-driven-release/references/rollback-procedures.md")
    HALT: "Production deployment failed. Execute rollback: ${PRODUCTION_DEPLOY_RESULT.rollback_command}"

Display: "Production deployment: SUCCESS"
Display: "Version: ${PRODUCTION_DEPLOY_RESULT.version}"
```
VERIFY: $PRODUCTION_DEPLOY_RESULT.success = true. If false, rollback triggered and workflow HALTED.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=05 --step=5.4 --project-root=.`

---

### Step 5.5: Wait for Deployment Rollout

EXECUTE: Monitor deployment rollout and wait for completion.
```
IF $DEPLOYMENT_STRATEGY == "canary":
    Display: "Canary deployment in progress..."
    Display: "Traffic: 5% -> 25% -> 50% -> 100%"
    # Monitor canary metrics at each stage
    Display: "Canary rollout complete"

ELIF $DEPLOYMENT_STRATEGY == "blue-green":
    Display: "Blue-green deployment: verifying green environment..."
    Display: "Green environment ready - switching traffic"
    Display: "Blue-green switch complete"

ELIF $DEPLOYMENT_STRATEGY == "rolling":
    Display: "Rolling deployment in progress..."
    Display: "Instances updated: tracking progress"
    Display: "Rolling deployment complete"

ELIF $DEPLOYMENT_STRATEGY == "recreate":
    Display: "Recreate deployment: stopping old, starting new..."
    Display: "New version started"

Display: "Deployment rollout complete for strategy: ${DEPLOYMENT_STRATEGY}"
```
VERIFY: Deployment rollout completed for the selected strategy.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=05 --step=5.5 --project-root=.`

---

### Step 5.6: Initial Production Health Check

EXECUTE: Run health check against production endpoints immediately after deployment.
```
FOR each endpoint in $PRODUCTION_DEPLOY_RESULT.endpoints:
    Bash(command="python .claude/skills/spec-driven-release/scripts/health_check.py --url=${endpoint} --timeout=30 --retries=3")

    IF exit_code != 0:
        Display: "Production health check FAILED: ${endpoint}"
        $PROD_HEALTH_FAILURES[] = endpoint
    ELSE:
        Display: "Production health check PASSED: ${endpoint}"

IF $PROD_HEALTH_FAILURES.length > 0:
    Display: "CRITICAL: Production health checks failing!"
    Read(file_path=".claude/skills/spec-driven-release/references/rollback-procedures.md")
    AskUserQuestion:
        Question: "Production health checks failed. Trigger immediate rollback?"
        Header: "Rollback"
        Options:
            - label: "Trigger rollback (Recommended)"
              description: "Revert to previous stable version immediately"
            - label: "Wait and retry"
              description: "Give deployment more time to stabilize"
        multiSelect: false

    IF user selects rollback:
        Bash(command="${PRODUCTION_DEPLOY_RESULT.rollback_command}")
        HALT: "Production rolled back due to health check failures"

Display: "Production health checks: ALL PASSED"
```
VERIFY: All production health checks passed OR rollback triggered.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=05 --step=5.6 --project-root=.`

---

### Step 5.7: Invoke Post-Production Hooks

EXECUTE: Trigger retrospective feedback hooks after production deployment. Non-blocking.
```
Read(file_path=".claude/skills/spec-driven-release/references/post-production-hooks.md")

$PROD_STATUS = $PRODUCTION_DEPLOY_RESULT.success ? "SUCCESS" : "FAILURE"

Bash(command="devforgeai-validate check-hooks --operation=release-production --status=${PROD_STATUS} 2>&1")

IF exit_code == 0:
    Display: "Post-production hooks eligible - invoking..."
    Bash(command="devforgeai-validate invoke-hooks --operation=release-production --context='environment=production,deployment_status=${PROD_STATUS},story_id=${STORY_ID}' 2>&1")
    Display: "Post-production hooks invoked (non-blocking)"
ELSE:
    Display: "Post-production hooks: not eligible (default: failures-only mode)"

# Non-blocking: hook failures do NOT affect deployment
```
VERIFY: Hook check completed. Hook invocation attempted if eligible. Failures logged but not blocking.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=05 --step=5.7 --project-root=.`

---

### Step 5.8: Display Production Deployment Status

EXECUTE: Show production deployment summary.
```
Display:
"
Production Deployment Summary
  Story: ${STORY_ID}
  Strategy: ${DEPLOYMENT_STRATEGY}
  Version: ${PRODUCTION_DEPLOY_RESULT.version}
  Endpoints: ${PRODUCTION_DEPLOY_RESULT.endpoints}
  Health Checks: ALL PASSED
  Security Audit: ${SECURITY_RESULTS.critical_count} critical, ${SECURITY_RESULTS.high_count} high
  Rollback Command: ${PRODUCTION_DEPLOY_RESULT.rollback_command}
"
```
VERIFY: Summary displayed with all deployment details.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=05 --step=5.8 --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --workflow=release --phase=05 --checkpoint-passed --project-root=.
```

## Phase 05 Completion Display

```
Phase 05 Complete: Production Deployment
  Strategy: ${DEPLOYMENT_STRATEGY}
  Version: ${PRODUCTION_DEPLOY_RESULT.version}
  Health: ALL PASSED
  Security: CLEARED
  Hooks: ${hooks_invoked ? 'Invoked' : 'Skipped'}
```
