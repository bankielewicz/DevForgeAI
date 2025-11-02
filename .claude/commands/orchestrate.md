---
description: Execute full story lifecycle end-to-end
argument-hint: [STORY-ID]
model: sonnet
allowed-tools: Read, Write, Edit, Skill, Glob
---

# /orchestrate - Complete Story Lifecycle Orchestration

Execute: Development → QA → Release (Staging → Production)

## Context

**Story:** @.ai_docs/Stories/$ARGUMENTS.story.md

---

## Phase 1: Story Validation & Checkpoint Detection

**Parse story metadata:**
1. Extract YAML frontmatter (id, status, title)
2. Check workflow history for checkpoints
3. Determine starting phase

**Valid Starting States:**
- "Ready for Dev" / "Backlog" → Start from Dev
- "Dev Complete" → Resume from QA
- "QA Approved" → Resume from Release
- "QA Failed" → Restart from Dev

**Invalid States (HALT):**
- "In Development" / "QA In Progress" / "Releasing" → Manual process running
- "Released" → Already complete

**Validation:**
- [ ] Story file exists
- [ ] Status allows orchestration
- [ ] Acceptance criteria defined

**Error Handling:**

Story not found:
```
ERROR: Story file not found: .ai_docs/Stories/$ARGUMENTS.story.md
Available stories: [Glob(pattern=".ai_docs/Stories/*.story.md")]
Use /create-story to create new story.
```

Invalid status:
```
ERROR: Cannot orchestrate story in status "{STATUS}"
Allowed: Ready for Dev, Backlog, Dev Complete, QA Approved, QA Failed
Use individual commands if manual process running: /dev, /qa, /release
```

**Checkpoint Detection:**

Check workflow history for checkpoints:
- "Checkpoint: DEV_COMPLETE" → Resume from Phase 3 (QA)
- "Checkpoint: QA_APPROVED" → Resume from Phase 4 (Release)
- "Checkpoint: STAGING_COMPLETE" → Resume from Phase 5 (Production)
- No checkpoint → Start from Phase 2 (Dev)

---

## Phase 2: Development

**Gate Check:**
```
IF checkpoint in ["DEV_COMPLETE", "QA_APPROVED", "STAGING_COMPLETE"]:
  Skip development (already complete)
ELSE:
  Execute development
```

**Invoke Skill:**
```
Skill(command="devforgeai-development --story=$ARGUMENTS")
```

**Expected Outcomes:**
- All tests pass (100% pass rate)
- Build succeeds
- Light QA validations passed
- Git commits created
- Story status = "Dev Complete"

**Failure Handling:**
```
ERROR: Development phase failed
[Skill error message]

Checkpoint saved: DEV_FAILED
Manual intervention required:
1. Review error
2. Run /dev {STORY-ID} to retry
3. Run /orchestrate {STORY-ID} to resume
```

**Success:**
```
Edit story:
- Workflow history: "Development completed"
- Checkpoint: "DEV_COMPLETE"
→ Proceed to Phase 3
```

---

## Phase 3: QA Validation

**Gate Check:**
```
IF checkpoint in ["QA_APPROVED", "STAGING_COMPLETE"]:
  Skip QA (already approved)
ELSE:
  Execute QA
```

**Pre-QA:**
- Verify status = "Dev Complete"
- Verify acceptance criteria exist

**Invoke Skill:**
```
Skill(command="devforgeai-qa --mode=deep --story=$ARGUMENTS")
```

**Expected Outcomes:**
- Coverage meets thresholds (95%/85%/80%)
- Zero CRITICAL violations
- Zero HIGH violations
- All acceptance criteria validated
- Story status = "QA Approved"

**Failure Handling:**
```
QA VALIDATION FAILED

Violations: [List from QA report]
Story status: QA Failed

Critical: {COUNT}, High: {COUNT}, Medium: {COUNT}, Low: {COUNT}

Orchestration HALTED.
Next steps:
1. Review: .devforgeai/qa/reports/{STORY-ID}-qa-report.md
2. Fix CRITICAL and HIGH violations
3. Run /dev {STORY-ID} to implement fixes
4. Run /orchestrate {STORY-ID} to resume
```

**Success:**
```
Edit story:
- Workflow history: "QA validation - APPROVED"
- Checkpoint: "QA_APPROVED"
→ Proceed to Phase 4
```

---

## Phase 4: Release - Staging

**Gate Check:**
```
REQUIRED: Story status = "QA Approved"
IF status != "QA Approved": HALT (QA approval mandatory)
```

**Invoke Skill:**
```
Skill(command="devforgeai-release --story=$ARGUMENTS --env=staging")
```

**Expected Outcomes:**
- Deployed to staging
- Smoke tests passed
- Health checks green
- Status remains "QA Approved"

**Failure Handling:**
```
STAGING DEPLOYMENT FAILED
[Error message]

Checkpoint: STAGING_FAILED
Production deployment BLOCKED.

Next steps:
1. Review deployment logs
2. Fix deployment config
3. Run /release {STORY-ID} --env=staging to retry
4. Run /orchestrate {STORY-ID} to resume
```

**Success:**
```
Edit story:
- Workflow history: "Staging deployment completed"
- Checkpoint: "STAGING_COMPLETE"
→ Proceed to Phase 5
```

---

## Phase 5: Release - Production

**Gate Check:**
```
REQUIRED: Staging deployment successful
IF checkpoint != "STAGING_COMPLETE": HALT
```

**Invoke Skill:**
```
Skill(command="devforgeai-release --story=$ARGUMENTS --env=production")
```

**Expected Outcomes:**
- Deployed to production
- Production smoke tests passed
- Production health checks green
- Story status = "Released"
- Release notes generated

**Failure Handling:**
```
PRODUCTION DEPLOYMENT FAILED
[Error message]

Rollback Status: [Auto-rollback triggered]
Story status: QA Approved (unchanged)
Checkpoint: PRODUCTION_FAILED

Next steps:
1. Verify rollback completed
2. Fix production deployment issues
3. Run /release {STORY-ID} --env=production to retry
4. Run /orchestrate {STORY-ID} to resume
```

**Success:**
```
Edit story:
- Workflow history: "Production deployment completed"
- Checkpoint: "PRODUCTION_COMPLETE"
→ Proceed to Phase 6
```

---

## Phase 6: Finalization

**Complete workflow documentation:**

Edit story file:
```markdown
## Workflow History (Updated by /orchestrate)

### Orchestration - {STORY-ID}
Started: {START_TIME}
Completed: {END_TIME}
Duration: {TOTAL_DURATION}

#### Phases:
- Development: ✅ ({DURATION}) - {TEST_COUNT} tests, 100% pass
- QA: ✅ ({DURATION}) - Coverage: {COVERAGE}%, Zero critical/high violations
- Staging: ✅ ({DURATION}) - Smoke tests passed, health green
- Production: ✅ ({DURATION}) - Live, health green

#### Final Status:
Status: Released ✅
Quality Gates: All passed
Deployment: Production live

#### Checkpoints:
{LIST_CHECKPOINTS}
```

**Update status:**
```yaml
status: "Released"
completed_date: {TIMESTAMP}
```

---

## Orchestration Complete

```
🎉 ORCHESTRATION COMPLETE - {STORY-ID}

✅ Development: Code implemented, 100% tests pass
✅ QA: All quality gates passed, zero violations
✅ Staging: Deployed and validated
✅ Production: Live with green health checks

Status: Released
Duration: {TOTAL_DURATION}

Story complete and deployed to production.
Monitor production metrics for 24 hours.
```

---

## Error Recovery

**Resume from Checkpoint:**

| Checkpoint | Action | Resume Command |
|------------|--------|----------------|
| DEV_FAILED | Fix issues, run /dev {ID} | /orchestrate {ID} |
| QA_FAILED | Fix violations, run /dev {ID} | /orchestrate {ID} |
| STAGING_FAILED | Fix config, run /release {ID} --env=staging | /orchestrate {ID} |
| PRODUCTION_FAILED | Fix issues, run /release {ID} --env=production | /orchestrate {ID} |

**Manual Phase Execution:**
```
/dev {STORY-ID}                      # Development only
/qa {STORY-ID}                       # QA only
/release {STORY-ID} --env=staging    # Staging only
/release {STORY-ID} --env=production # Production only
```

---

## Token Budget

| Phase | Tokens |
|-------|--------|
| Validation | ~2K |
| Development (Skill summary) | ~5K |
| QA (Skill summary) | ~5K |
| Staging (Skill summary) | ~3K |
| Production (Skill summary) | ~3K |
| Finalization | ~2K |
| **TOTAL** | **~20K** |

Skill invocations create isolated contexts. Main conversation receives summaries only.

---

## Integration

**Skill Dependencies:**
- devforgeai-development (Phase 2)
- devforgeai-qa (Phase 3)
- devforgeai-release (Phases 4-5)

**Quality Gates:**
- Gate 1: Test Passing (Dev → QA)
- Gate 2: QA Approval (QA → Release)
- Gate 3: Staging Success (Staging → Production)

**Prerequisites:**
- All 6 context files exist (use /create-context)
- Story in valid starting state

---

## Usage Examples

**Full orchestration:**
```
> /orchestrate STORY-042
Starting: Dev → QA → Release
Phase 2: Dev ✅ (45 min)
Phase 3: QA ✅ (12 min)
Phase 4: Staging ✅ (8 min)
Phase 5: Production ✅ (10 min)
🎉 Story STORY-042 released to production!
```

**Resume from QA failure:**
```
> /orchestrate STORY-042
Checkpoint: QA_FAILED
Resuming from Development...
Phase 2: Dev ✅ (30 min)
Phase 3: QA ✅ (10 min)
Phase 4: Staging ✅ (8 min)
Phase 5: Production ✅ (10 min)
🎉 Story STORY-042 released to production!
```

**Resume from staging failure:**
```
> /orchestrate STORY-042
Checkpoint: STAGING_FAILED
Skipping Dev and QA (complete)
Resuming from Staging...
Phase 4: Staging ✅ (8 min)
Phase 5: Production ✅ (10 min)
🎉 Story STORY-042 released to production!
```

---

**Version:** 1.0 | **Created:** 2025-10-31 | **Phase 3 Command 9/9**
