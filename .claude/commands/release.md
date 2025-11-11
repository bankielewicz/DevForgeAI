---
description: Deploy story to staging and production
argument-hint: [STORY-ID] [environment]
# Environment: 'staging' or 'production' (no -- prefix)
model: sonnet
allowed-tools: Read, Write, Edit, Glob, Skill, Task, Bash(docker:*), Bash(kubectl:*), Bash(git:*)
---

# Release Command

Deploy QA-approved stories to staging or production environments with automated validation, smoke testing, and rollback capabilities.

## Context

Load story file and deployment configuration:

```context
@.ai_docs/Stories/$1.story.md
@.devforgeai/deployment/config.json
@.devforgeai/context/tech-stack.md
```

## Pre-Execution Validation

### Phase 0: Argument Validation

**Extract arguments:**
```
STORY_ID = $1
ENV_ARG = $2 (optional)
```

**Validate story ID format:**
```
IF $1 is empty OR does NOT match pattern "STORY-[0-9]+":
  AskUserQuestion:
  Question: "Story ID '$1' doesn't match format STORY-NNN. What story should I release?"
  Header: "Story ID"
  Options:
    - "List stories in QA Approved status"
    - "List stories in Dev Complete status"
    - "Show correct /release command syntax"
  multiSelect: false

  Extract STORY_ID from user response
```

**Validate story file exists:**
```
Glob(pattern=".ai_docs/Stories/${STORY_ID}*.story.md")

IF no matches found:
  AskUserQuestion:
  Question: "Story ${STORY_ID} not found. What should I do?"
  Header: "Story not found"
  Options:
    - "List all available stories"
    - "Cancel command"
  multiSelect: false
```

**Parse environment argument:**
```
IF $2 provided:
  IF $2 in ["staging", "production", "prod", "stage"]:
    # Normalize
    IF $2 in ["prod", "production"]:
      ENVIRONMENT = "production"
    ELSE:
      ENVIRONMENT = "staging"

  ELSE IF $2 starts with "--env=":
    # User used flag syntax (educate them)
    EXTRACTED_ENV = substring after "--env="

    IF EXTRACTED_ENV in ["staging", "production"]:
      ENVIRONMENT = EXTRACTED_ENV
      Note to user: "Flag syntax (--env=) not needed. Use: /release STORY-001 production"

    ELSE:
      AskUserQuestion:
      Question: "Unknown environment in flag: $2. Where should I deploy?"
      Header: "Deployment target"
      Options:
        - "staging (test environment)"
        - "production (live environment)"
      multiSelect: false

  ELSE IF $2 starts with "--":
    # Unknown flag
    AskUserQuestion:
    Question: "Unknown flag: $2. Where should I deploy?"
    Header: "Deployment target"
    Options:
      - "staging (test environment first)"
      - "production (skip staging - risky!)"
    multiSelect: false

  ELSE:
    # Unknown value
    AskUserQuestion:
    Question: "Unknown environment: $2. Where should I deploy?"
    Header: "Deployment target"
    Options:
      - "staging (safe choice)"
      - "production (requires QA approval)"
    multiSelect: false

ELSE:
  # No environment specified - default to staging (safe choice)
  ENVIRONMENT = "staging"
  Note to user: "Defaulting to staging. Use '/release STORY-001 production' for production deployment."
```

**Validation summary:**
```
✓ Story ID: ${STORY_ID}
✓ Story file: ${STORY_FILE}
✓ Environment: ${ENVIRONMENT}
✓ Proceeding with deployment...
```

---

## Workflow

### Phase 1: Pre-Release Validation (Gate Checks)

**Objective:** Verify story is ready for deployment

**Steps:**

1. **Parse Story YAML Frontmatter**
   ```yaml
   id: STORY-XXX
   title: Story Title
   status: QA Approved  # REQUIRED
   epic: EPIC-XXX
   sprint: SPRINT-XXX
   priority: High
   ```

2. **Verify QA Approval Status**
   - Read story frontmatter
   - Check `status: QA Approved`
   - **HALT if not approved:** "Story {STORY-ID} is not QA Approved. Current status: {status}. Run /qa command first."

3. **Check Prerequisite Stories**
   - Parse story dependencies (if defined in frontmatter or specification)
   - Verify prerequisite stories have `status: Released`
   - **HALT if dependencies not met:** "Cannot deploy {STORY-ID}. Prerequisite stories not released: {list}"

4. **Read Deployment Configuration**
   - Load `.devforgeai/deployment/config.json`
   - Verify environment configuration exists (staging/production)
   - **HALT if config missing:** "Deployment configuration not found. Expected: .devforgeai/deployment/config.json"

5. **Final Security Scan**
   - Invoke Task for security audit before production deployment
   ```
   Task(
     subagent_type="security-auditor",
     prompt="Perform final security scan for story {STORY-ID} before production deployment. Check for:
     - Hardcoded secrets or API keys
     - SQL injection vulnerabilities
     - XSS vulnerabilities
     - Insecure dependencies
     - Authentication/authorization issues
     Return PASS/FAIL with findings."
   )
   ```
   - **HALT if FAIL:** "Security scan failed. Address findings before deployment: {findings}"

**Success Criteria:**
- ✅ Story status is "QA Approved"
- ✅ All prerequisite stories deployed
- ✅ Deployment config exists and valid
- ✅ Security scan passed

---

### Phase 2: Production Deployment Confirmation

**Objective:** Confirm production deployment if applicable

**Steps:**

1. **Check if Production Deployment**
   - If ${ENVIRONMENT} == "production", display confirmation:
     ```
     ⚠️  PRODUCTION DEPLOYMENT
     Story: {STORY-ID}
     Title: {title}
     Target: Production environment

     This will deploy to production. Continue? (yes/no)
     ```
   - Use AskUserQuestion for explicit confirmation
   - **HALT if not confirmed:** "Production deployment cancelled by user"

2. **Load Environment Configuration**
   - Extract environment-specific settings from config.json for ${ENVIRONMENT}:
     ```json
     {
       "staging": {
         "platform": "kubernetes",
         "cluster": "staging-cluster",
         "namespace": "app-staging",
         "deployment_strategy": "rolling"
       },
       "production": {
         "platform": "kubernetes",
         "cluster": "prod-cluster",
         "namespace": "app-prod",
         "deployment_strategy": "blue-green"
       }
     }
     ```

**Success Criteria:**
- ✅ Environment determined (staging or production)
- ✅ Environment configuration loaded
- ✅ Production deployment confirmed (if applicable)

---

### Phase 3: Invoke Release Skill

**Objective:** Execute deployment via devforgeai-release skill

**Steps:**

1. **Prepare Skill Invocation**
   - Build command: `devforgeai-release --story={STORY-ID} --env={env}`
   - Display pre-deployment summary:
     ```
     🚀 DEPLOYMENT SUMMARY
     Story: {STORY-ID} - {title}
     Environment: {env}
     Platform: {platform}
     Strategy: {deployment_strategy}

     Starting deployment...
     ```

2. **Invoke Release Skill**

   **Context for skill:**
   - Story content loaded via @file reference above
   - Story ID: ${STORY_ID}
   - Environment: ${ENVIRONMENT}

   ```
   Skill(command="devforgeai-release")
   ```

   **After skill invocation:**
   - Skill's SKILL.md content expands inline in conversation
   - **YOU execute the skill's workflow phases** (not waiting for external result)
   - Follow the skill's instructions phase by phase
   - Produce output as skill instructs

   **The skill instructs you to execute 6-phase deployment process:**
     - **Phase 1:** Pre-Release Validation (verify QA approval, tests passing, build success)
     - **Phase 2:** Staging Deployment (if env=staging)
     - **Phase 3:** Production Deployment (if env=production)
     - **Phase 4:** Post-Deployment Validation (smoke tests, health checks)
     - **Phase 5:** Release Documentation (release notes, changelog)
     - **Phase 6:** Post-Release Monitoring (metrics collection, alerting setup)

   **Expected outputs from skill execution:**
   - Deployment status (SUCCESS/FAILED)
   - Smoke test results
   - Deployment artifacts (release notes, changelog)
   - Rollback command (if needed)

**Success Criteria:**
- ✅ Release skill invoked successfully
- ✅ Skill execution completed without errors
- ✅ Deployment artifacts generated

---

### Phase 4: Verify Deployment

**Objective:** Confirm deployment success and validate production readiness

**Steps:**

1. **Check Deployment Status**
   - Parse skill output for deployment result
   - Verify deployment command completed successfully
   - Check application health endpoints
   - **HALT if failed:** "Deployment failed. See error details: {error}"

2. **Verify Smoke Tests Passed**
   - Read smoke test results from `.devforgeai/qa/smoke-tests/{STORY-ID}-{env}-results.json`
   - Expected format:
     ```json
     {
       "story_id": "STORY-001",
       "environment": "production",
       "timestamp": "2025-10-31T10:30:00Z",
       "status": "PASSED",
       "tests": [
         {"name": "Health Check", "status": "PASSED"},
         {"name": "API Authentication", "status": "PASSED"},
         {"name": "Critical Path", "status": "PASSED"}
       ]
     }
     ```
   - **TRIGGER ROLLBACK if failed:** "Smoke tests failed. Initiating rollback..."

3. **Verify Story Status Updated**
   - Read story file YAML frontmatter
   - Check status updated to `Released`
   - Verify workflow history includes release entry
   - **WARN if not updated:** "Story status not updated. Manual verification required."

4. **Check Monitoring Alerts**
   - If production deployment, check for immediate alerts
   - Monitor error rates (should not exceed 2x baseline)
   - Monitor response times (should meet SLA)
   - **TRIGGER ROLLBACK if alerts:** "Production alerts detected. Initiating rollback..."

**Success Criteria:**
- ✅ Deployment completed successfully
- ✅ Smoke tests passed (100% pass rate)
- ✅ Story status updated to "Released"
- ✅ No production alerts triggered

---

### Phase 5: Display Results

**Objective:** Provide deployment summary and next steps

**Steps:**

1. **Display Deployment Summary**
   ```markdown
   ✅ DEPLOYMENT SUCCESSFUL

   Story: {STORY-ID} - {title}
   Environment: {env}
   Deployment Time: {timestamp}
   Strategy: {deployment_strategy}

   📊 Smoke Test Results:
   - Health Check: ✅ PASSED
   - API Authentication: ✅ PASSED
   - Critical Path: ✅ PASSED

   Total Tests: {total}
   Passed: {passed}
   Failed: {failed}
   Pass Rate: {pass_rate}%
   ```

2. **Show Release Notes Location**
   ```markdown
   📝 Release Documentation:
   - Release Notes: .devforgeai/releases/{STORY-ID}-release-notes.md
   - Changelog: CHANGELOG.md (updated)
   - Story File: .ai_docs/Stories/{STORY-ID}.story.md (status: Released)
   ```

3. **Display Rollback Command (If Needed)**
   - If production deployment, provide rollback command:
     ```markdown
     🔄 Rollback Command (if issues arise):
     /rollback {STORY-ID} --env=production

     Or use platform-specific command:
     kubectl rollout undo deployment/{deployment-name} -n {namespace}
     ```

4. **Show Post-Deployment Monitoring**
   ```markdown
   📈 Post-Deployment Monitoring:
   - Monitor dashboard: {monitoring_url}
   - Error rate baseline: {baseline_error_rate}
   - Current error rate: {current_error_rate}
   - Response time P95: {p95_response_time}ms

   Alert thresholds:
   - Error rate > {threshold}
   - Response time > {threshold}ms
   - Failed requests > {threshold}%
   ```

5. **Provide Next Steps**
   ```markdown
   🎯 Next Steps:
   1. Monitor production metrics for 24 hours
   2. Review post-deployment alerts (if any)
   3. Schedule retrospective for story {STORY-ID}
   4. Update sprint burndown chart

   Sprint Progress:
   - Stories Completed: {completed}/{total}
   - Stories Released: {released}/{total}
   - Sprint Velocity: {velocity} points
   ```

**Success Criteria:**
- ✅ Deployment summary displayed
- ✅ Release notes location provided
- ✅ Rollback command documented
- ✅ Monitoring guidance provided

---

## Error Handling

### Error: Story Not QA Approved

**Symptom:** Story status is not "QA Approved"

**Response:**
```markdown
❌ DEPLOYMENT BLOCKED

Story {STORY-ID} is not ready for deployment.
Current Status: {current_status}
Required Status: QA Approved

Next Steps:
1. Run /qa command to validate story
2. Fix any quality violations
3. Ensure QA approval before deployment

Command: /qa {STORY-ID} --mode=deep
```

---

### Error: Deployment Failure

**Symptom:** Deployment command failed or returned error

**Response:**
```markdown
❌ DEPLOYMENT FAILED

Story: {STORY-ID}
Environment: {env}
Error: {error_message}

Troubleshooting:
1. Check deployment logs: {log_location}
2. Verify environment configuration: .devforgeai/deployment/config.json
3. Check platform status: {platform_status_url}
4. Verify credentials and permissions

Rollback Status: {rollback_status}
```

**Actions:**
1. Capture full error output
2. Save to `.devforgeai/releases/{STORY-ID}-deployment-error.log`
3. Do NOT update story status
4. Notify user of failure and next steps

---

### Error: Smoke Test Failure

**Symptom:** Smoke tests failed after deployment

**Response:**
```markdown
❌ SMOKE TESTS FAILED - INITIATING ROLLBACK

Story: {STORY-ID}
Environment: {env}
Failed Tests: {failed_test_count}

Failed Test Details:
{list_of_failed_tests}

Automatic Rollback:
- Reverting deployment to previous version
- Restoring previous configuration
- Updating story status to "Release Failed"

Rollback Status: {rollback_status}
```

**Actions:**
1. **Trigger automatic rollback**
   - Invoke Skill(command="devforgeai-release --story={STORY-ID} --env={env} --rollback")
   - Or use platform-specific rollback command
2. **Update story status to "Release Failed"**
3. **Create hotfix story** (if critical bug detected)
4. **Notify team** of rollback

---

### Error: Environment Not Configured

**Symptom:** Deployment configuration missing for specified environment

**Response:**
```markdown
❌ ENVIRONMENT NOT CONFIGURED

Environment: {env}
Configuration File: .devforgeai/deployment/config.json

The specified environment is not configured in deployment config.

Available Environments:
{list_of_configured_environments}

Next Steps:
1. Add environment configuration to .devforgeai/deployment/config.json
2. Or run deployment to available environment
3. Or invoke devforgeai-architecture skill to set up environment

Example Configuration:
{
  "{env}": {
    "platform": "kubernetes",
    "cluster": "{cluster-name}",
    "namespace": "{namespace}",
    "deployment_strategy": "rolling"
  }
}
```

---

### Error: Prerequisite Stories Not Deployed

**Symptom:** Story has dependencies that are not yet released

**Response:**
```markdown
❌ DEPLOYMENT BLOCKED - DEPENDENCIES NOT MET

Story: {STORY-ID}
Prerequisite Stories Not Released:
{list_of_unreleased_prerequisites}

Dependency Chain:
{prerequisite_1} → {prerequisite_2} → {STORY-ID}

Next Steps:
1. Deploy prerequisite stories first
2. Or remove dependencies if not required
3. Or update story specification to remove dependency

Commands:
/release {prerequisite_1}
/release {prerequisite_2}
/release {STORY-ID}
```

---

## Success Criteria

- [ ] **Pre-release validation passed** - QA approved, dependencies met, security scan passed
- [ ] **Environment determined** - Staging or production environment identified
- [ ] **Deployment executed** - Release skill invoked and completed successfully
- [ ] **Smoke tests passed** - All smoke tests passed (100% pass rate)
- [ ] **Story status updated** - Status changed to "Released"
- [ ] **Release notes generated** - Release documentation created
- [ ] **Monitoring configured** - Post-deployment monitoring active
- [ ] **Rollback command available** - Rollback procedure documented

---

## Token Efficiency

**Target:** <35K tokens per invocation

**Optimization Strategies:**

1. **Use native tools for file operations:**
   - ✅ Read(file_path="...") instead of Bash cat
   - ✅ Edit(...) instead of Bash sed
   - ✅ Glob(pattern="...") instead of Bash find

2. **Cache frequently accessed files:**
   - Story file (read once, parse multiple times)
   - Deployment config (read once, reference throughout)
   - Context files (load only if needed)

3. **Parallel tool invocations:**
   - Read story file AND deployment config in same call
   - Verify smoke tests AND story status in same call

4. **Focused validation:**
   - Don't re-validate QA approval (already done in Phase 1)
   - Don't re-read files unnecessarily

---

## Integration with DevForgeAI Framework

**Invoked by:**
- User via `/release` command
- devforgeai-orchestration skill (coordinated sprint releases)

**Invokes:**
- **devforgeai-release skill** (core deployment logic)
- **Task(subagent_type="security-auditor")** (final security scan)
- **Skill(command="devforgeai-release --rollback")** (if smoke tests fail)

**Updates:**
- Story status in `.ai_docs/Stories/{STORY-ID}.story.md`
- Workflow history in story file
- Release notes in `.devforgeai/releases/{STORY-ID}-release-notes.md`
- Changelog in `CHANGELOG.md`

**Dependencies:**
- `.devforgeai/deployment/config.json` (deployment configuration)
- `.devforgeai/smoke-tests/config.json` (smoke test configuration)
- `.devforgeai/context/tech-stack.md` (platform information)
- `.ai_docs/Stories/{STORY-ID}.story.md` (story specification)

---

## Example Usage

**Deploy to staging (default):**
```
/release STORY-001
```

**Deploy to production:**
```
/release STORY-001 --env=production
```

**Coordinated sprint release:**
```
/release SPRINT-001 --env=production
```
(Deploys all QA-approved stories in sprint)

---

## Related Commands

- `/qa` - Run quality validation before release
- `/rollback` - Revert failed deployment
- `/dev` - Implement story with TDD workflow
- `/orchestrate` - Manage story workflow and progression

---

**Last Updated:** 2025-10-31
**Status:** Production Ready
**Model:** Sonnet
**Token Budget:** <35K
