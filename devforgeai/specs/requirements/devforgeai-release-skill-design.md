# DevForgeAI Release Skill - Design Specification

**Date Created:** 2025-10-30
**Status:** Design Phase
**Purpose:** Define the release management skill that completes the DevForgeAI spec-driven development workflow

---

## Executive Summary

The **devforgeai-release** skill is the **final stage** of the DevForgeAI framework. It manages the transition from QA-approved code to production deployment, ensuring safe, repeatable, and auditable releases.

**Key Capabilities:**
1. **Release Validation** - Verify QA approval and readiness gates
2. **Deployment Orchestration** - Execute deployment across environments
3. **Smoke Testing** - Validate deployment success
4. **Rollback Management** - Handle failed deployments gracefully
5. **Release Documentation** - Generate release notes and changelog
6. **Multi-Environment Support** - Dev → Staging → Production pipeline

**Integration Point:** Final step after devforgeai-qa approval, updates story status to "Released"

---

## 1. Skill Metadata (SKILL.md Frontmatter)

```yaml
---
name: devforgeai-release
description: Orchestrate production releases with deployment automation, smoke testing, rollback capabilities, and release documentation. Use after QA approval to deploy stories to production. Supports multiple deployment strategies (blue-green, canary, rolling) and environments (staging, production). Enforces release gates and maintains deployment audit trail.
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
```

---

## 2. Skill Purpose & Philosophy

### Purpose Statement

This skill manages the **release workflow** from QA-approved code to production deployment. It ensures that:

1. **Only QA-approved code reaches production**
2. **Deployments are repeatable and automated**
3. **Failures are detected early with smoke tests**
4. **Rollbacks are quick and safe**
5. **Release documentation is complete**
6. **Audit trail exists for compliance**

### Philosophy

**"Deploy with Confidence, Fail Gracefully"**

- **Confidence:** Automated checks at every stage
- **Graceful Failure:** Detect issues early, rollback quickly
- **Repeatability:** Same process every time
- **Auditability:** Complete deployment history

**"Safety Over Speed"**

- Never skip release gates
- Validate deployment health before declaring success
- Prefer staged rollouts over big-bang deploys

**"Environment Parity"**

- Staging should mirror production
- Test deployment in staging first
- Validate infrastructure-as-code changes

---

## 3. When to Use This Skill

**Trigger Scenarios:**

✅ **After QA Approval:**
- Story status = "QA Approved"
- All quality gates passed
- Ready to deploy to production

✅ **Coordinated Sprint Releases:**
- Multiple stories released together
- End-of-sprint deployment
- Feature flag activation

✅ **Hotfix Deployments:**
- Critical bug fix bypasses normal sprint cycle
- Still requires QA approval (light validation minimum)
- Fast-tracked deployment

✅ **Rollback Operations:**
- Production issue detected
- Revert to previous stable version

❌ **When NOT to Use:**
- Story not QA-approved (must pass QA first)
- Missing deployment configuration
- Production maintenance window not available

---

## 4. Release Workflow (6 Phases)

### Phase 1: Pre-Release Validation

**Objective:** Verify release readiness before deployment

#### 1.1 Load Story and QA Report

```
# Load story document
Read(file_path="devforgeai/specs/Stories/{story_id}.story.md")

# Parse frontmatter
story_metadata = extract_yaml_frontmatter(story)
  - id
  - title
  - status (must be "QA Approved")
  - epic
  - sprint

# Load QA report
Read(file_path=".devforgeai/qa/reports/{story_id}-qa-report.md")

# Parse QA status
qa_status = extract_qa_status(qa_report)
```

#### 1.2 Validate Release Gates

**Gate 1: QA Approval Gate**
```
CHECKS:
  ✓ Story status == "QA Approved"
  ✓ QA report exists
  ✓ QA report status == "PASS"
  ✓ Zero CRITICAL violations
  ✓ Zero HIGH violations (or approved exceptions)

IF any_check_fails:
    BLOCK: "Story not ready for release"
    Report: "Release gate failed: [reason]"
    Action: Return to QA or development
```

**Gate 2: Dependency Gate**
```
CHECKS:
  ✓ No blocking dependencies (prerequisite stories released)
  ✓ No conflicting releases in progress
  ✓ Database migrations prepared (if needed)

IF dependencies_exist:
    AskUserQuestion:
    Question: "Story {story_id} depends on {prerequisite_stories}. Are these deployed?"
    Header: "Dependencies"
    Options:
      - "Yes, all dependencies deployed"
      - "No, deploy dependencies first"
      - "Proceed anyway (risk)"
    multiSelect: false
```

**Gate 3: Environment Readiness Gate**
```
CHECKS:
  ✓ Staging environment available
  ✓ Production environment available
  ✓ No maintenance window conflicts
  ✓ Deployment credentials valid

# Check environment health
Bash(command="kubectl get pods --namespace=production")  # Kubernetes
# OR
Bash(command="az webapp show --name {app} --resource-group {rg}")  # Azure
# OR
Bash(command="aws ecs describe-services --cluster {cluster}")  # AWS
```

#### 1.3 Determine Deployment Strategy

**Use AskUserQuestion to select strategy:**

```
Question: "Which deployment strategy should be used for {story_id}?"
Header: "Deployment strategy"
Description: "Different strategies balance risk and speed"
Options:
  - "Blue-Green (zero downtime, instant rollback)"
  - "Rolling Update (gradual, resource-efficient)"
  - "Canary (partial traffic, progressive rollout)"
  - "Recreate (downtime acceptable, simple)"
multiSelect: false
```

**Strategy Characteristics:**

**Blue-Green:**
- Two identical environments (blue = current, green = new)
- Deploy to green, test, switch traffic
- Instant rollback (switch back to blue)
- Resource cost: 2x infrastructure during deployment

**Rolling Update:**
- Gradually replace old instances with new
- No downtime
- Rollback: Deploy previous version
- Resource cost: Minimal overhead

**Canary:**
- Deploy to small subset (5-10% traffic)
- Monitor metrics, gradually increase traffic
- Rollback: Stop canary, keep baseline
- Resource cost: Minimal overhead

**Recreate:**
- Stop old version, deploy new version
- Downtime during deployment
- Rollback: Redeploy old version
- Resource cost: None (simplest)

---

### Phase 2: Staging Deployment

**Objective:** Deploy to staging environment and validate

#### 2.1 Prepare Deployment Artifacts

**Git Workflow:**
```
# Ensure on correct branch
Bash(command="git status")

# Create release branch from main
Bash(command="git checkout main")
Bash(command="git pull origin main")
Bash(command="git checkout -b release/{story_id}")

# Tag release
version = generate_version()  # e.g., v1.2.3 or story-001-release
Bash(command=f"git tag -a {version} -m 'Release {story_id}: {story_title}'")
Bash(command=f"git push origin {version}")
```

**Build Artifacts:**
```
# .NET
Bash(command="dotnet publish -c Release -o ./publish")

# Node.js
Bash(command="npm run build")

# Python
Bash(command="pip install -r requirements.txt")

# Docker
Bash(command=f"docker build -t {image_name}:{version} .")
Bash(command=f"docker push {registry}/{image_name}:{version}")
```

#### 2.2 Deploy to Staging

**Deployment methods based on infrastructure:**

**Kubernetes (Helm/Kubectl):**
```
# Update image tag in deployment
Bash(command=f"helm upgrade {release_name} ./chart --set image.tag={version} --namespace=staging")

# OR kubectl
Bash(command=f"kubectl set image deployment/{deployment_name} {container_name}={image}:{version} --namespace=staging")

# Wait for rollout
Bash(command=f"kubectl rollout status deployment/{deployment_name} --namespace=staging --timeout=5m")
```

**Azure App Service:**
```
# Deploy via Azure CLI
Bash(command=f"az webapp deployment source config-zip --resource-group {rg} --name {app_name}-staging --src ./publish.zip")

# Wait for deployment
Bash(command=f"az webapp show --name {app_name}-staging --resource-group {rg} --query state")
```

**AWS ECS:**
```
# Update task definition
Bash(command=f"aws ecs register-task-definition --cli-input-json file://task-def.json")

# Update service
Bash(command=f"aws ecs update-service --cluster {cluster} --service {service}-staging --task-definition {task_def}:{version}")

# Wait for stability
Bash(command=f"aws ecs wait services-stable --cluster {cluster} --services {service}-staging")
```

**Serverless (AWS Lambda):**
```
# Deploy function
Bash(command=f"aws lambda update-function-code --function-name {function_name}-staging --zip-file fileb://function.zip")

# Update alias
Bash(command=f"aws lambda update-alias --function-name {function_name} --name staging --function-version $LATEST")
```

**Traditional VPS (Ansible/Terraform):**
```
# Run Ansible playbook
Bash(command="ansible-playbook deploy-staging.yml -i inventory/staging")

# OR Terraform apply
Bash(command="terraform apply -target=module.staging -auto-approve")
```

#### 2.3 Smoke Test Staging Deployment

**Automated Health Checks:**

```
# Wait for application to start
sleep(30)  # Allow startup time

# Health endpoint check
health_url = get_staging_url() + "/health"
response = curl(health_url)

IF response.status_code != 200:
    FAIL: "Staging health check failed"
    Action: Rollback staging deployment
```

**Functional Smoke Tests:**

```
# Test critical user flows
smoke_tests = [
    "test_user_login_works",
    "test_api_endpoints_respond",
    "test_database_connectivity",
    "test_external_integrations"
]

FOR each test in smoke_tests:
    Bash(command=f"pytest tests/smoke/{test}.py --environment=staging")

IF any_test_fails:
    FAIL: "Smoke test failed in staging"
    Report: "Failed tests: [test names]"
    Action: Rollback staging deployment
    BLOCK: Fix issues before production deployment
```

**Manual Validation (Optional):**

```
AskUserQuestion:
Question: "Staging deployment complete. Smoke tests passed. Perform manual validation?"
Header: "Manual testing"
Description: f"Staging URL: {staging_url}"
Options:
  - "Manual testing complete - proceed to production"
  - "Issues found - rollback staging"
  - "Skip manual testing - proceed to production"
multiSelect: false
```

---

### Phase 3: Production Deployment

**Objective:** Deploy to production using selected strategy

#### 3.1 Final Pre-Production Checks

**Confirmation Gate:**
```
AskUserQuestion:
Question: "Ready to deploy {story_id} to PRODUCTION using {strategy} strategy?"
Header: "Production deployment"
Description: "This will deploy version {version} to production environment"
Options:
  - "Yes, proceed with production deployment"
  - "No, abort (need more testing)"
  - "Wait (not ready yet)"
multiSelect: false

IF user_says_no:
    ABORT: Log decision, keep staging deployed for testing
```

**Backup Current State:**
```
# Capture current production state for rollback
current_version = get_current_production_version()
backup_db = should_backup_database()

IF backup_db:
    Bash(command="./scripts/backup_database.sh production")
    Report: "Database backup created: {backup_id}"
```

#### 3.2 Execute Deployment Strategy

**Blue-Green Deployment:**
```
# Deploy to green environment (inactive)
Bash(command=f"helm upgrade {release_name}-green ./chart --set image.tag={version} --namespace=production-green")

# Wait for green to be healthy
Bash(command=f"kubectl rollout status deployment/{deployment_name} --namespace=production-green --timeout=5m")

# Run smoke tests against green
run_smoke_tests(environment="production-green")

IF smoke_tests_pass:
    # Switch traffic from blue to green
    Bash(command=f"kubectl patch service/{service_name} -p '{{\"spec\":{{\"selector\":{{\"version\":\"green\"}}}}}}'")

    # Monitor for 5 minutes
    monitor_metrics(duration=300, environment="production")

    IF metrics_healthy:
        Report: "✅ Blue-Green deployment successful"
        # Scale down blue (keep for quick rollback)
    ELSE:
        Report: "❌ Production metrics degraded"
        # Switch back to blue
        Bash(command=f"kubectl patch service/{service_name} -p '{{\"spec\":{{\"selector\":{{\"version\":\"blue\"}}}}}}'")
        ROLLBACK
ELSE:
    FAIL: "Smoke tests failed in production-green"
    ROLLBACK: Delete green deployment
```

**Rolling Update Deployment:**
```
# Update deployment with rolling update strategy
Bash(command=f"kubectl set image deployment/{deployment_name} {container}={image}:{version} --namespace=production")

# Monitor rollout progress
Bash(command=f"kubectl rollout status deployment/{deployment_name} --namespace=production --timeout=10m")

# Gradually updates pods (25% at a time by default)
# Monitors health checks, pauses if failures

IF rollout_successful:
    Report: "✅ Rolling update successful"
ELSE:
    Report: "❌ Rolling update failed"
    Bash(command=f"kubectl rollout undo deployment/{deployment_name} --namespace=production")
    ROLLBACK
```

**Canary Deployment:**
```
# Deploy canary version (5% traffic)
Bash(command=f"helm upgrade {release_name}-canary ./chart --set image.tag={version} --set replicaCount=1 --namespace=production")

# Configure traffic split (95% baseline, 5% canary)
Bash(command=f"kubectl apply -f canary-traffic-split.yaml")

# Monitor canary metrics for 10 minutes
metrics = monitor_canary_metrics(duration=600, canary_percentage=5)

IF metrics.error_rate < baseline_error_rate * 1.1:  # Within 10% of baseline
    # Increase canary to 25%
    update_traffic_split(canary_percentage=25)
    metrics = monitor_canary_metrics(duration=600, canary_percentage=25)

    IF metrics_healthy:
        # Increase canary to 50%
        update_traffic_split(canary_percentage=50)
        metrics = monitor_canary_metrics(duration=600, canary_percentage=50)

        IF metrics_healthy:
            # Complete rollout to 100%
            Bash(command=f"kubectl scale deployment/{deployment_name} --replicas=0 --namespace=production")  # Scale down baseline
            Bash(command=f"kubectl scale deployment/{deployment_name}-canary --replicas={target_replicas}")
            Report: "✅ Canary rollout successful"
        ELSE:
            ROLLBACK: "Metrics degraded at 50% canary"
    ELSE:
        ROLLBACK: "Metrics degraded at 25% canary"
ELSE:
    ROLLBACK: "Canary error rate too high at 5%"
```

**Recreate Deployment:**
```
# Scale down current version
Bash(command=f"kubectl scale deployment/{deployment_name} --replicas=0 --namespace=production")

# Wait for pods to terminate
sleep(30)

# Deploy new version
Bash(command=f"kubectl set image deployment/{deployment_name} {container}={image}:{version} --namespace=production")
Bash(command=f"kubectl scale deployment/{deployment_name} --replicas={target_replicas} --namespace=production")

# Wait for new pods to be ready
Bash(command=f"kubectl rollout status deployment/{deployment_name} --namespace=production --timeout=5m")

IF rollout_successful:
    Report: "✅ Recreate deployment successful"
ELSE:
    FAIL: "Deployment failed"
    # Rollback to previous version
    Bash(command=f"kubectl set image deployment/{deployment_name} {container}={image}:{previous_version}")
    ROLLBACK
```

---

### Phase 4: Post-Deployment Validation

**Objective:** Verify production deployment health

#### 4.1 Production Smoke Tests

**Run critical path tests:**

```
# Wait for application to stabilize
sleep(60)

# Production health check
production_url = get_production_url()
health_response = curl(production_url + "/health")

IF health_response.status != 200:
    CRITICAL: "Production health check failed"
    ROLLBACK

# Run smoke tests against production
Bash(command="pytest tests/smoke/ --environment=production")

IF smoke_tests_fail:
    CRITICAL: "Production smoke tests failed"
    Report: "Failed tests: [list]"
    ROLLBACK
```

#### 4.2 Metrics Monitoring

**Monitor key metrics for initial period:**

```
# Monitor for 10-15 minutes post-deployment
metrics_window = 900  # 15 minutes

metrics = collect_metrics(
    environment="production",
    duration=metrics_window,
    metrics=[
        "error_rate",
        "response_time_p95",
        "cpu_utilization",
        "memory_usage",
        "request_rate",
        "database_query_time"
    ]
)

# Compare against baseline (pre-deployment metrics)
baseline = load_baseline_metrics()

CHECKS:
  ✓ error_rate < baseline_error_rate * 1.2  # Within 20% of baseline
  ✓ response_time_p95 < baseline_p95 * 1.3  # Within 30% of baseline
  ✓ cpu_utilization < 80%  # Not overloaded
  ✓ memory_usage < 85%  # Not memory-starved

IF any_metric_exceeds_threshold:
    WARNING: "Production metrics degraded"
    Report: "Metrics: [detailed report]"

    AskUserQuestion:
    Question: "Production metrics show degradation. How to proceed?"
    Header: "Metrics warning"
    Options:
      - "Continue monitoring (acceptable degradation)"
      - "Rollback immediately (unacceptable)"
      - "Investigate before deciding"
    multiSelect: false

    IF user_says_rollback:
        ROLLBACK
```

#### 4.3 User Acceptance Validation (Optional)

**For high-risk deployments:**

```
AskUserQuestion:
Question: "Production deployment complete. Smoke tests passed. Perform user acceptance testing?"
Header: "UAT"
Description: "Verify functionality with real users before declaring release successful"
Options:
  - "UAT complete - release successful"
  - "Issues found - rollback"
  - "Skip UAT - declare success"
multiSelect: false
```

---

### Phase 5: Release Documentation

**Objective:** Document release for audit trail and communication

#### 5.1 Generate Release Notes

```
Write(file_path=".devforgeai/releases/release-{version}.md", content="""
# Release {version} - {date}

## Story: {story_id} - {story_title}

### Changes
{extract_changes_from_story()}

### Acceptance Criteria Met
{list_acceptance_criteria_from_story()}

### QA Validation
- QA Status: PASS
- Test Coverage: {coverage_percentage}%
- Zero CRITICAL violations
- Zero HIGH violations

### Deployment Details
- **Version:** {version}
- **Git Tag:** {git_tag}
- **Git Commit:** {commit_sha}
- **Deployment Strategy:** {strategy}
- **Deployed By:** {deployer_name}
- **Deployed At:** {timestamp}

### Environments
- **Staging:** Deployed {staging_timestamp}, Smoke tests: PASS
- **Production:** Deployed {production_timestamp}, Smoke tests: PASS

### Metrics (Post-Deployment)
- Error Rate: {error_rate} (Baseline: {baseline_error_rate})
- Response Time (p95): {p95_response_time}ms (Baseline: {baseline_p95}ms)
- CPU Utilization: {cpu_percent}%
- Memory Usage: {memory_percent}%

### Rollback Plan
- **Previous Version:** {previous_version}
- **Rollback Command:** `{rollback_command}`
- **Database Backup:** {backup_id} (if applicable)

### Post-Release Monitoring
- [ ] Monitor error rates for 24 hours
- [ ] Check user feedback channels
- [ ] Review production logs

### Notes
{additional_notes}
""")
```

#### 5.2 Update Story Status

```
# Update story frontmatter
Edit(file_path="devforgeai/specs/Stories/{story_id}.story.md",
     old_string="status: QA Approved",
     new_string="status: Released")

# Check workflow box
Edit(file_path="devforgeai/specs/Stories/{story_id}.story.md",
     old_string="- [ ] Released",
     new_string="- [x] Released")

# Add release metadata
Edit(file_path="devforgeai/specs/Stories/{story_id}.story.md",
     old_string="created: {created_date}",
     new_string=f"created: {created_date}\nreleased: {release_date}\nversion: {version}")

# Append workflow history
history_entry = f"""
### {timestamp} - Released
- **Previous Status:** QA Approved
- **Action Taken:** Production deployment via {strategy} strategy
- **Version:** {version}
- **Deployment:** Successful
- **Smoke Tests:** PASS
- **Metrics:** Within acceptable thresholds
- **Release Notes:** .devforgeai/releases/release-{version}.md
"""

# Append to workflow history section
Edit(file_path="devforgeai/specs/Stories/{story_id}.story.md",
     old_string="## Workflow History\n\n",
     new_string=f"## Workflow History\n\n{history_entry}\n")
```

#### 5.3 Update Sprint Progress

```
# If story was part of a sprint, update sprint document
Read(file_path="devforgeai/specs/Sprints/{sprint_id}.sprint.md")

# Mark story as complete
Edit(file_path="devforgeai/specs/Sprints/{sprint_id}.sprint.md",
     old_string=f"- [ ] {story_id}:",
     new_string=f"- [x] {story_id}:")

# Update velocity metrics
# Calculate completed points vs. sprint capacity
```

#### 5.4 Generate Changelog (Cumulative)

```
# Append to project changelog
Edit(file_path="CHANGELOG.md",
     old_string="## [Unreleased]",
     new_string=f"""## [Unreleased]

## [{version}] - {date}

### Added
{list_added_features()}

### Changed
{list_changed_features()}

### Fixed
{list_bug_fixes()}

### Deployment
- Story: {story_id}
- QA Coverage: {coverage}%
- Deployment: {strategy} strategy
""")
```

---

### Phase 6: Post-Release Monitoring & Closure

**Objective:** Monitor production stability and close release

#### 6.1 Set Up Monitoring Alerts

```
# Configure alerts for post-release monitoring
alert_config = {
    "error_rate_threshold": baseline_error_rate * 1.5,
    "response_time_threshold": baseline_p95 * 1.5,
    "duration": "24 hours",
    "notification": "email/slack"
}

# Implementation depends on monitoring stack
# Example: CloudWatch, Datadog, Prometheus
```

#### 6.2 Schedule Post-Deployment Review

```
# Create follow-up task
Write(file_path=".devforgeai/post-release/{story_id}-review.md", content="""
# Post-Release Review: {story_id}

**Review Date:** {date + 24h}

## Checklist
- [ ] Review 24-hour error rates
- [ ] Check user feedback/support tickets
- [ ] Review production logs for anomalies
- [ ] Validate metrics against baseline
- [ ] Document lessons learned

## Actions If Issues Found
- [ ] Create hotfix story
- [ ] Plan rollback if critical
- [ ] Update monitoring thresholds

## Sign-Off
- [ ] Tech Lead approval
- [ ] Product Owner notification
""")
```

#### 6.3 Report Release Success

```
Report: f"""
════════════════════════════════════════════════
✅ Release Successful: {story_id}
════════════════════════════════════════════════

Version: {version}
Deployed: {timestamp}
Strategy: {strategy}

Environments:
  ✓ Staging: Deployed and validated
  ✓ Production: Deployed and validated

Validation:
  ✓ Smoke tests: PASS
  ✓ Health checks: PASS
  ✓ Metrics: Within thresholds

Documentation:
  ✓ Release notes: .devforgeai/releases/release-{version}.md
  ✓ Story updated: Status = Released
  ✓ Changelog updated

Post-Release:
  - Monitoring alerts configured (24h)
  - Post-release review scheduled
  - Rollback plan documented

Next Steps:
  1. Monitor production for 24 hours
  2. Conduct post-release review
  3. Start next story in sprint

────────────────────────────────────────────────
"""
```

---

## 5. Rollback Procedures

### Automatic Rollback Triggers

**Immediate Rollback If:**
- Health check fails (HTTP 500+)
- Smoke test fails
- Error rate > 2x baseline
- Critical service unavailable
- Database migration fails (with data loss risk)

### Rollback Execution

**Kubernetes:**
```
# Rollback to previous revision
Bash(command=f"kubectl rollout undo deployment/{deployment_name} --namespace=production")

# Verify rollback
Bash(command=f"kubectl rollout status deployment/{deployment_name} --namespace=production")
```

**Azure App Service:**
```
# Swap slots back
Bash(command=f"az webapp deployment slot swap --slot staging --name {app_name} --resource-group {rg} --target-slot production --action=swap")
```

**Docker/ECS:**
```
# Revert to previous task definition
Bash(command=f"aws ecs update-service --cluster {cluster} --service {service} --task-definition {previous_task_def}")
```

**Database Rollback:**
```
# If migration was applied
Bash(command="./scripts/rollback_migration.sh {migration_id}")

# Restore from backup (if necessary)
Bash(command=f"./scripts/restore_database.sh {backup_id}")
```

### Post-Rollback Actions

```
# Update story status
Edit(file_path="devforgeai/specs/Stories/{story_id}.story.md",
     old_string="status: Releasing",
     new_string="status: QA Approved")

# Document rollback
Write(file_path=".devforgeai/releases/rollback-{version}.md", content="""
# Rollback: {version}

**Reason:** {rollback_reason}
**Rolled Back At:** {timestamp}
**Previous Version Restored:** {previous_version}

## Root Cause
{describe_issue}

## Actions Taken
- Production rolled back to {previous_version}
- Database restored (if applicable)
- Alerts cleared

## Next Steps
- [ ] Fix issue in development
- [ ] Re-run QA validation
- [ ] Plan re-deployment
""")

# Create hotfix story if needed
AskUserQuestion:
Question: "Rollback complete. Create hotfix story for the issue?"
Header: "Hotfix needed"
Options:
  - "Yes, create hotfix story"
  - "No, fix in next sprint"
multiSelect: false
```

---

## 6. Bundled Resources

### 6.1 Reference Files (`references/`)

**deployment-strategies.md**
- Detailed comparison of blue-green, rolling, canary, recreate
- When to use each strategy
- Infrastructure requirements

**smoke-testing-guide.md**
- Standard smoke test checklist
- Critical path testing
- API contract validation

**rollback-procedures.md**
- Platform-specific rollback commands
- Database rollback strategies
- Disaster recovery procedures

**monitoring-metrics.md**
- Key metrics to monitor post-deployment
- Baseline establishment techniques
- Alert threshold configuration

**release-checklist.md**
- Pre-deployment checklist
- Deployment checklist
- Post-deployment checklist

### 6.2 Asset Templates (`assets/templates/`)

**release-notes-template.md**
- Standardized release notes format

**rollback-plan-template.md**
- Rollback documentation template

**deployment-config-template.yaml**
- Kubernetes/Helm deployment configuration

### 6.3 Scripts (`scripts/`)

**health_check.py**
- HTTP health endpoint checker
- Retry logic with exponential backoff
- Multi-endpoint validation

**smoke_test_runner.py**
- Orchestrates smoke test suite
- Environment-specific configuration
- Parallel test execution

**metrics_collector.py**
- Collect metrics from monitoring systems
- Compare against baseline
- Generate metrics report

**rollback_automation.sh**
- Automated rollback for various platforms
- Database backup/restore
- Configuration management

**release_notes_generator.py**
- Generate release notes from story documents
- Changelog aggregation
- Markdown formatting

---

## 7. AskUserQuestion Patterns

### Pattern 1: Deployment Strategy Selection

```
CONTEXT:
- Story approved for release
- Multiple strategies available

AskUserQuestion:
Question: "Which deployment strategy for {story_id}?"
Header: "Deployment strategy"
Description: "Blue-Green = instant rollback, Canary = progressive, Rolling = gradual"
Options:
  - "Blue-Green (zero downtime, 2x resources)"
  - "Rolling Update (gradual, minimal resources)"
  - "Canary (5% → 25% → 50% → 100%)"
  - "Recreate (simple, brief downtime OK)"
multiSelect: false
```

### Pattern 2: Degraded Metrics Decision

```
CONTEXT:
- Deployment complete
- Metrics show 25% increase in error rate (within 2x threshold)

AskUserQuestion:
Question: "Error rate increased from 0.1% to 0.13% (+30%). How to proceed?"
Header: "Metrics degradation"
Description: "Within threshold but higher than baseline"
Options:
  - "Acceptable - continue monitoring"
  - "Rollback - unacceptable increase"
  - "Investigate logs before deciding"
multiSelect: false
```

### Pattern 3: Hotfix vs. Standard Release

```
CONTEXT:
- Critical bug in production
- Fix available and QA-approved

AskUserQuestion:
Question: "This is a critical bug fix. Expedite deployment?"
Header: "Hotfix deployment"
Description: "Hotfix bypasses normal release schedule"
Options:
  - "Yes - deploy immediately (hotfix process)"
  - "No - wait for next scheduled release"
  - "Deploy to staging first, then fast-track"
multiSelect: false
```

### Pattern 4: Rollback Confirmation

```
CONTEXT:
- Deployment experiencing issues
- Automatic rollback triggered

AskUserQuestion:
Question: "Deployment failed smoke tests. Rollback to {previous_version}?"
Header: "Rollback confirmation"
Description: "Production will revert to previous stable version"
Options:
  - "Yes - rollback immediately"
  - "No - try to fix forward (risky)"
  - "Investigate first (production affected during investigation)"
multiSelect: false
```

---

## 8. Integration with Other Skills

### From devforgeai-qa

**Handoff Data:**
- Story ID with status "QA Approved"
- QA report with PASS status
- Test coverage metrics
- Zero critical/high violations

### To devforgeai-orchestration

**Updates:**
- Story status changed to "Released"
- Workflow history updated
- Sprint progress updated (if applicable)

**Orchestration then:**
- Marks story as complete
- Updates sprint velocity
- Triggers next story in queue

---

## 9. Success Criteria

**Release skill succeeds when:**

- [ ] QA approval validated
- [ ] Staging deployment successful
- [ ] Production deployment successful
- [ ] Smoke tests pass (staging + production)
- [ ] Metrics within acceptable thresholds
- [ ] Release notes generated
- [ ] Story status updated to "Released"
- [ ] Changelog updated
- [ ] Monitoring configured
- [ ] No rollback required

**Output Artifacts:**
- Release notes (`.devforgeai/releases/release-{version}.md`)
- Updated story document (status = "Released")
- Updated changelog (`CHANGELOG.md`)
- Deployment logs
- Post-release monitoring alert configuration

---

## 10. Multi-Environment Support

### Environment Progression

```
Development → Staging → Production
     ↓            ↓          ↓
   (Local)    (Pre-Prod)  (Live)
```

**Environment Configuration:**
- Different URLs, credentials, resource limits
- Environment-specific smoke tests
- Separate monitoring dashboards

### Environment Parity

**Ensure staging mirrors production:**
- Same OS, runtime versions
- Same database engine/version
- Same infrastructure (containers, load balancers)
- Same monitoring/logging configuration

**Detect parity issues:**
```
# Compare configurations
config_diff = compare_environments("staging", "production")

IF config_diff.has_differences:
    WARNING: "Staging differs from production"
    Report: "Differences: {config_diff}"
    AskUserQuestion: "Proceed anyway or fix parity first?"
```

---

## 11. Notes & Best Practices

**Always Deploy to Staging First:**
- Never skip staging validation
- Staging is the "dress rehearsal"

**Smoke Tests Are Mandatory:**
- Even for "simple" changes
- Catch deployment issues early

**Monitor First Hour Closely:**
- Most issues surface within 60 minutes
- Have rollback plan ready

**Document Everything:**
- Release notes for every deployment
- Rollback reasons if they occur
- Lessons learned

**Feature Flags for Large Changes:**
- Deploy code with feature disabled
- Enable feature progressively
- Instant disable if issues occur

---

## 12. Future Enhancements

**Potential Additions:**
- Automated canary analysis (ML-driven)
- Progressive feature flag rollout
- A/B testing integration
- Cost analysis (cloud spend per deployment)
- Compliance validation (SOC2, HIPAA audit trail)
- Integration with incident management (PagerDuty, Opsgenie)

---

**End of Design Specification**
