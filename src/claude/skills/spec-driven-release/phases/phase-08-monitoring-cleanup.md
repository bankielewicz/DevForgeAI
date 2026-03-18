# Phase 08: Monitoring, Cleanup & Closure

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --workflow=release --from=07 --to=08 --project-root=.
```

## Contract

PURPOSE: Configure post-release monitoring (for deployable projects), clean up session checkpoint, display execution summary.
REQUIRED SUBAGENTS: none
REQUIRED ARTIFACTS: Monitoring configuration (if applicable), checkpoint cleanup status, execution summary
STEP COUNT: 6 mandatory steps

---

## Mandatory Steps

### Step 8.1: Check Monitoring Applicability

EXECUTE: Determine if monitoring steps apply based on project type.
```
IF $PROJECT_TYPE == "library":
    $MONITORING_APPLICABLE = false
    Display: "Monitoring setup skipped: Library project - no running services to monitor"
    Display: "Proceeding to cleanup steps only"
ELSE:
    $MONITORING_APPLICABLE = true
    Display: "Monitoring applicable for ${PROJECT_TYPE} project"
```
VERIFY: $MONITORING_APPLICABLE is set (true for cli/api, false for library).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=08 --step=8.1 --project-root=.`

---

### Step 8.2: Load Monitoring References

EXECUTE: Load monitoring references. Required even if monitoring is not applicable (anti-skip enforcement).
```
Read(file_path=".claude/skills/spec-driven-release/references/monitoring-closure.md")
Read(file_path=".claude/skills/spec-driven-release/references/monitoring-metrics.md")

IF $MONITORING_APPLICABLE == false:
    Display: "References loaded (mandatory) but monitoring steps will be skipped"
```
VERIFY: Both reference files loaded successfully (non-empty Read responses).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=08 --step=8.2 --project-root=.`

---

### Step 8.3: Configure Post-Release Monitoring

EXECUTE: Set up monitoring for deployed services. Skip for library projects.
```
IF $MONITORING_APPLICABLE == false:
    Display: "Step 8.3 skipped: No services to monitor (library project)"
ELSE:
    # Error tracking setup
    Display: "Configuring error tracking..."
    Display: "  Error rate threshold: < 1% (alert if exceeded)"
    Display: "  Error tracking: enabled for ${PRODUCTION_DEPLOY_RESULT.endpoints}"

    # Performance monitoring
    Display: "Configuring performance monitoring..."
    Display: "  Response time SLA: < 500ms p95"
    Display: "  Throughput baseline: capture current"

    # Alerting rules
    Display: "Configuring alerting rules..."
    Display: "  Alert on: error rate > 1%, response time > 1000ms, 5xx rate > 0.5%"
    Display: "  Alert channels: configured per devforgeai/config/monitoring.yaml"

    Display: "Post-release monitoring configured"
```
VERIFY: Either monitoring configured (for cli/api) OR explicitly skipped (for library).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=08 --step=8.3 --project-root=.`

---

### Step 8.4: Schedule Post-Deployment Review

EXECUTE: Create reminder for 24-hour post-deployment review.
```
IF $MONITORING_APPLICABLE == false:
    Display: "Step 8.4 skipped: No deployment to review (library project)"
ELSE:
    Display:
    "
    Post-Deployment Review Checklist (24 hours):
      [ ] Error rates remain below threshold
      [ ] Response times within SLA
      [ ] No unexpected resource usage spikes
      [ ] User feedback reviewed
      [ ] Rollback plan still accessible: ${PRODUCTION_DEPLOY_RESULT.rollback_command}

    Review scheduled for: ${NOW + 24 hours}
    "
```
VERIFY: Either review checklist displayed (for cli/api) OR explicitly skipped (for library).
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=08 --step=8.4 --project-root=.`

---

### Step 8.5: Session Checkpoint Cleanup

EXECUTE: Delete session checkpoint for the released story. Always runs (all project types).
```
# Attempt checkpoint cleanup via Python API
Bash(command="python3 -c \"
from devforgeai_cli.session.checkpoint import delete_checkpoint
if delete_checkpoint('${STORY_ID}'):
    print('Session checkpoint cleaned up')
else:
    print('No checkpoint to clean up')
\" 2>&1")

IF exit_code != 0:
    # Fallback: try direct file deletion
    Glob(pattern="devforgeai/workflows/${STORY_ID}*.json")
    IF checkpoint files found:
        FOR each checkpoint_file:
            Display: "Manual cleanup needed: ${checkpoint_file}"
    ELSE:
        Display: "No checkpoint files found (already clean)"
ELSE:
    Display: "Session checkpoint cleanup: ${stdout}"
```
VERIFY: Either checkpoint deleted successfully OR no checkpoint existed OR cleanup noted for manual action.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=08 --step=8.5 --project-root=.`

---

### Step 8.6: Display Execution Summary

EXECUTE: Show complete release workflow summary. Always runs (all project types).
```
# Calculate total phases completed vs skipped
$COMPLETED_PHASES = phases where status = "completed"
$SKIPPED_PHASES = phases where status = "skipped"

Display:
"
================================================================
  RELEASE COMPLETE: ${STORY_ID}
================================================================

  Project Type: ${PROJECT_TYPE}
  Environment: ${ENVIRONMENT}
  Strategy: ${DEPLOYMENT_STRATEGY}

  Phase Summary:
  | Phase | Name                          | Status    |
  |-------|-------------------------------|-----------|
  | 01    | Setup & Classification        | Completed |
  | 02    | Build & Package               | ${phase_02_status} |
  | 03    | Pre-Release Validation        | Completed |
  | 04    | Staging Deployment            | ${phase_04_status} |
  | 05    | Production Deployment         | ${phase_05_status} |
  | 06    | Post-Deployment Validation    | ${phase_06_status} |
  | 07    | Release Documentation         | Completed |
  | 08    | Monitoring, Cleanup & Closure | Completed |

  Artifacts:
    Release Notes: devforgeai/releases/release-${VERSION}-${STORY_ID}.md
    Story Archive: devforgeai/specs/Stories/archive/${STORY_ID}.story.md
    Story Status: Released

  Next Steps:
    1. Monitor deployment for 24 hours (if applicable)
    2. Review post-deployment checklist
    3. Plan next story in sprint

================================================================
"
```
VERIFY: Execution summary displayed with all phases, artifacts, and next steps.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase=08 --step=8.6 --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --workflow=release --phase=08 --checkpoint-passed --project-root=.
```

## Phase 08 Completion Display

```
Phase 08 Complete: Monitoring, Cleanup & Closure
  Monitoring: ${MONITORING_APPLICABLE ? 'Configured' : 'Skipped (library)'}
  Checkpoint: Cleaned up
  Status: RELEASE WORKFLOW COMPLETE
  Story ${STORY_ID} is now Released
```
