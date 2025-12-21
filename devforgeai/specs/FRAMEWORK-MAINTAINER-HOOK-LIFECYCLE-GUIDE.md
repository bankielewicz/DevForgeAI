# Framework Maintainer Guide: Hook Lifecycle for Epic Creation

**Purpose:** Guide for framework maintainers on the epic creation hook system architecture, lifecycle, and maintenance

**Related:** STORY-028 (Wire Hooks Into /create-epic Command), EPIC-006 (Feedback System Integration)

**Audience:** DevForgeAI framework maintainers, contributors extending hook system

---

## Hook Lifecycle Overview

### What is the Epic Creation Hook?

The **post-epic-create feedback hook** is an optional, non-blocking retrospective system that triggers after successful epic creation (Phase 4A.9 in devforgeai-orchestration skill).

**Purpose:**
- Capture feedback on epic quality while details are fresh
- Validate feature decomposition granularity (3-8 feature range)
- Assess complexity scoring accuracy (0-10 scale)
- Identify missing risks or unclear success criteria
- Improve future epic planning through insights

**Design Principles:**
1. **Non-blocking:** Hook failures never break epic creation (always exits 0)
2. **Optional:** Disabled by default, user opts in via configuration
3. **Contextual:** Questions reference actual epic data ({feature_count}, {complexity_score})
4. **Fast:** <3 second overhead target (hook check <100ms, invoke <500ms)
5. **Safe:** Input validation prevents command injection

---

## Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ /create-epic Command (Lean Orchestration)                      │
│  - Phase 0: Argument validation                                │
│  - Phase 1: Set context markers                                │
│  - Phase 2: Invoke devforgeai-orchestration skill              │
│  - Phase 3: Display results                                    │
└────────────────────┬────────────────────────────────────────────┘
                     │ Skill(command="devforgeai-orchestration")
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│ devforgeai-orchestration Skill (Epic Creation Mode)            │
│  Phase 4A.1: Epic Discovery (generate EPIC-ID)                 │
│  Phase 4A.2: Context Gathering (goal, timeline, stakeholders)  │
│  Phase 4A.3: Feature Decomposition (requirements-analyst)      │
│  Phase 4A.4: Technical Assessment (architect-reviewer)         │
│  Phase 4A.5: Epic File Creation (write .epic.md) ← PREREQUISITE
│  Phase 4A.6: Requirements Spec (optional)                      │
│  Phase 4A.7: Validation & Self-Healing ← PREREQUISITE          │
│  Phase 4A.8: Completion Summary                                │
│  Phase 4A.9: Post-Epic Feedback Hook ← THIS STORY              │
│             │                                                   │
│             ├─ Step 1: Check hook config (enabled?)            │
│             ├─ Step 2: Parse configuration (timeout, etc.)     │
│             ├─ Step 3: Validate epic context (file exists?)    │
│             ├─ Step 4: Invoke hook subprocess (background)     │
│             ├─ Step 5: Monitor execution (timeout handling)    │
│             └─ Step 6: Handle errors gracefully (exit 0)       │
└────────────────────┬────────────────────────────────────────────┘
                     │ devforgeai invoke-hooks --operation=epic-create --epic-id=EPIC-XXX
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│ devforgeai CLI (Hook Invocation)                               │
│  - Load hooks.yaml configuration                               │
│  - Read epic file (devforgeai/specs/Epics/EPIC-XXX-*.epic.md)         │
│  - Extract epic metadata (features, complexity, risks)         │
│  - Render questions with placeholders ({feature_count})        │
│  - Present questions via AskUserQuestion                       │
│  - Save responses to devforgeai/feedback/epic-create/        │
│  - Update feedback-index.json                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Hook Lifecycle Phases

### Phase 1: Hook Registration (Configuration)

**File:** `devforgeai/config/hooks.yaml`

**Maintainer Action:** Add epic-create hook definition

**Example:**
```yaml
- id: post-epic-create-feedback
  name: "Post-Epic Creation Feedback"
  operation_type: command
  operation_pattern: "create-epic"
  trigger_status: [success]
  feedback_type: conversation
  enabled: false  # Set to true when ready
```

**Validation:**
```bash
# Verify configuration is valid YAML
python -c "import yaml; yaml.safe_load(open('devforgeai/config/hooks.yaml'))"

# Verify hook recognized by CLI
devforgeai check-hooks --operation=epic-create --status=success
```

---

### Phase 2: Hook Availability Check (Skill Step 4A.9.1)

**Triggered:** After Phase 4A.7 (Epic Validation) completes successfully

**CLI Command:** `devforgeai check-hooks --operation=epic-create --status=success`

**Expected Response:**
```json
{
  "enabled": true,
  "available": true,
  "timeout": 30000,
  "trigger_conditions_met": true
}
```

**Performance Target:** <100ms (p95)

**Exit Codes:**
- `0` - Hooks enabled and available
- `1` - Hooks disabled in configuration
- `2` - Configuration error (malformed YAML)

**Maintainer Note:** This check is fast and cached (configuration loaded once per process).

---

### Phase 3: Epic Context Validation (Skill Step 4A.9.3)

**Purpose:** Ensure epic file exists and epic ID is valid before CLI invocation

**Validation Checks:**
1. Epic file exists: `devforgeai/specs/Epics/$EPIC_ID-*.epic.md`
2. Epic ID format: `^EPIC-[0-9]{3}$` (EPIC-001 through EPIC-999)

**Security:** Regex validation prevents command injection

**Error Handling:**
- File missing → Skip hook, log warning, continue
- Invalid ID → Skip hook, log error, continue
- All errors → Exit 0 (non-blocking)

**Maintainer Note:** Never skip validation - it's the security boundary.

---

### Phase 4: Hook Invocation (Skill Step 4A.9.4)

**CLI Command:**
```bash
timeout $HOOK_TIMEOUT_SECONDS devforgeai invoke-hooks \
  --operation=epic-create \
  --epic-id="$EPIC_ID" \
  --timeout=$HOOK_TIMEOUT &
```

**Process Management:**
- Runs in background (`&` suffix)
- Timeout enforced (default 30s, configurable)
- PID captured for monitoring

**Epic Context Passed:**
- `--epic-id=EPIC-XXX` (CLI reads epic file for metadata)
- Epic file path: `devforgeai/specs/Epics/EPIC-XXX-*.epic.md`
- Metadata extracted: features, complexity, risks, stakeholders, success criteria

**CLI Responsibilities:**
1. Read epic file
2. Extract metadata (parse YAML frontmatter + markdown sections)
3. Render questions with placeholders ({feature_count} → actual count)
4. Present questions via AskUserQuestion
5. Save responses to `devforgeai/feedback/epic-create/EPIC-XXX-{timestamp}.json`
6. Update feedback index (feedback-index.json)

---

### Phase 5: Hook Completion Monitoring (Skill Step 4A.9.5)

**Purpose:** Wait for hook to complete or timeout gracefully

**Monitoring Pattern:**
```bash
if wait $HOOK_PID 2>/dev/null; then
  # Hook completed successfully
  HOOK_EXIT_CODE=$?
  echo "Hook completed - exit_code=$HOOK_EXIT_CODE" >> hooks.log
else
  # Hook still running or timed out
  # Continue to Phase 4A.8 (non-blocking design)
fi
```

**Timeout Handling:**
- `timeout` command sends SIGTERM after N seconds
- If process doesn't exit, sends SIGKILL
- Exit code 124 indicates timeout
- Skill logs timeout, continues successfully

**Performance Note:** Hook may complete after Phase 4A.8 finishes (background process).

---

### Phase 6: Error Handling (Skill Step 4A.9.6)

**Comprehensive Error Matrix:**

| Exit Code | Meaning | Action | Epic Creation Result |
|-----------|---------|--------|----------------------|
| 0 | Success | Log success | ✅ Continue (exit 0) |
| 1 | CLI not found | Log warning | ✅ Continue (exit 0) |
| 2 | Invalid epic ID | Log error | ✅ Continue (exit 0) |
| 3 | Epic file missing | Log error | ✅ Continue (exit 0) |
| 124 | Timeout | Kill process, log | ✅ Continue (exit 0) |
| Other | Unknown error | Log error | ✅ Continue (exit 0) |

**Logging Requirements:**

**Success Log Format:**
```
[2025-11-16T14:32:45Z] INFO: Hook invoked - operation=epic-create epic-id=EPIC-001 pid=12345
[2025-11-16T14:32:46Z] INFO: Hook completed - exit_code=0 duration=1200ms
```

**Error Log Format:**
```
[2025-11-16T14:32:47Z] ERROR: Hook failed - operation=epic-create epic-id=EPIC-001 exit_code=1 error="CLI not found"
[2025-11-16T14:32:48Z] WARNING: Hook timed out after 30s - epic-id=EPIC-002
```

**Maintainer Note:** All error paths MUST return exit 0 to preserve non-blocking design.

---

## Maintainer Responsibilities

### 1. Configuration Management

**Maintainer Tasks:**
- Review `devforgeai/config/hooks.yaml.example` for new hook patterns
- Update hooks.yaml with team-specific configurations
- Document custom questions in hook metadata
- Archive old configurations before major changes

**Configuration Versioning:**
```bash
# Before making changes, backup current config
cp devforgeai/config/hooks.yaml devforgeai/config/hooks.yaml.backup-$(date +%Y%m%d)

# After changes, validate
python -c "import yaml; yaml.safe_load(open('devforgeai/config/hooks.yaml'))"

# Commit configuration changes
git add devforgeai/config/hooks.yaml
git commit -m "config: Update epic-create hook settings"
```

---

### 2. Performance Monitoring

**Metrics to Track:**
- Hook check latency (target: <100ms p95)
- Hook invocation latency (target: <500ms p95)
- Total overhead (target: <3000ms p95)
- Hook success rate (target: >95%)
- Hook timeout rate (target: <5%)

**Monitoring Commands:**
```bash
# Calculate average hook check duration
grep "check-hooks" devforgeai/feedback/.logs/hooks.log | \
  grep "duration=" | \
  sed 's/.*duration=\([0-9]*\)ms.*/\1/' | \
  awk '{sum+=$1; count++} END {print "Average: " sum/count " ms"}'

# Count hook failures
grep "ERROR" devforgeai/feedback/.logs/hook-errors.log | wc -l

# Check timeout rate
total=$(grep "Hook invoked" devforgeai/feedback/.logs/hooks.log | wc -l)
timeouts=$(grep "timed out" devforgeai/feedback/.logs/hooks.log | wc -l)
echo "Timeout rate: $(echo "scale=2; $timeouts / $total * 100" | bc)%"
```

**Alert Thresholds:**
- Hook check >150ms (p95) → Investigate configuration loading
- Total overhead >5s → Investigate CLI startup or network
- Timeout rate >10% → Increase timeout or optimize feedback script
- Failure rate >5% → Review error logs, fix recurring issues

---

### 3. Log Management

**Log Files:**
- Success: `devforgeai/feedback/.logs/hooks.log`
- Errors: `devforgeai/feedback/.logs/hook-errors.log`
- Feedback sessions: `devforgeai/feedback/epic-create/EPIC-XXX-{timestamp}.json`

**Rotation Strategy:**
```bash
# Monthly log rotation (add to cron or CI/CD)
#!/bin/bash
ARCHIVE_DIR="devforgeai/feedback/.archives/$(date +%Y-%m)"
mkdir -p "$ARCHIVE_DIR"

# Archive and compress old logs
tar -czf "$ARCHIVE_DIR/hooks-$(date +%Y-%m).tar.gz" \
  devforgeai/feedback/.logs/hooks.log \
  devforgeai/feedback/.logs/hook-errors.log

# Truncate logs after archive
> devforgeai/feedback/.logs/hooks.log
> devforgeai/feedback/.logs/hook-errors.log

echo "Logs archived to $ARCHIVE_DIR"
```

**Retention Policy:**
- Keep current month logs uncompressed
- Compress previous months (tar.gz)
- Retain 12 months of archived logs
- Delete logs >12 months old

---

### 4. Testing Hook Integration

**Test Checklist:**

**Unit Tests (37 tests):**
```bash
# Run unit tests for hook configuration, CLI mocking, validation
pytest tests/unit/test_create_epic_hooks.py -v

# Expected: All 37 tests pass
```

**Integration Tests (12 tests):**
```bash
# Run E2E tests for complete hook workflow
pytest tests/integration/test_create_epic_hooks_e2e.py -v

# Expected: 10/12 pass (2 CLI integration tests may fail if CLI signature differs)
```

**Performance Tests (23 tests):**
```bash
# Run performance validation
pytest tests/performance/test_create_epic_hooks_performance.py -v

# Expected: Hook check <100ms, total overhead <3000ms
```

**Manual Smoke Test:**
```bash
# 1. Enable epic-create hooks
# Edit devforgeai/config/hooks.yaml: set enabled: true

# 2. Create test epic
/create-epic "Test Epic for Hook Validation"

# 3. Verify hook triggered
# Should see: Retrospective questions about epic quality

# 4. Check feedback saved
ls -la devforgeai/feedback/epic-create/

# 5. Disable hooks
# Edit hooks.yaml: set enabled: false
```

---

## Hook Integration Points

### 1. Command Layer (.claude/commands/create-epic.md)

**Responsibility:** Display hook results (Phase 4 in command, <20 lines)

**Implementation:**
```markdown
### Phase 4: Display Results

Output: result.summary (from skill)

IF result.hook_triggered:
  Display: "✅ Feedback captured for {epic_id}"
ELIF result.hook_disabled:
  Display: "" (no message - hooks optional)
ELIF result.hook_failed:
  Display: "⚠️ Feedback hook unavailable (continuing)"
```

**Maintainer Note:** Command should NOT contain hook logic (only display).

---

### 2. Skill Layer (.claude/skills/devforgeai-orchestration/SKILL.md)

**Responsibility:** Phase 4A.9 implementation (all hook logic)

**Location:** Lines 252-510 (258 lines)

**Key Sections:**
- **Overview:** Purpose and characteristics (lines 254-263)
- **Execution Flow:** 6 steps (lines 265-445)
- **Logging Requirements:** Structured log formats (lines 448-461)
- **Data Flow Diagram:** Visual workflow (lines 463-488)
- **Integration Notes:** Lean orchestration pattern (lines 490-497)
- **Success Criteria:** 8 checkpoints (lines 499-509)

**Maintainer Responsibilities:**
- Keep Phase 4A.9 synchronized with CLI signature changes
- Update error handling when new exit codes added
- Maintain performance targets (update if CLI optimized)
- Document changes in phase section comments

---

### 3. CLI Layer (.claude/scripts/devforgeai_cli/)

**Commands:**
- `devforgeai check-hooks --operation=epic-create --status=success`
- `devforgeai invoke-hooks --operation=epic-create --epic-id=EPIC-XXX`

**Maintainer Responsibilities:**
- Maintain CLI signature compatibility (breaking changes require skill updates)
- Keep configuration schema synchronized (hooks.yaml structure)
- Document exit codes in CLI README
- Optimize performance (target: check <100ms, invoke <500ms)

**CLI Source:**
- Check hooks: `.claude/scripts/devforgeai_cli/commands/check_hooks.py`
- Invoke hooks: `.claude/scripts/devforgeai_cli/commands/invoke_hooks.py`

---

## Adding New Hook Types

### Example: Add post-sprint-create Hook

**Step 1: Update hooks.yaml.example**

```yaml
# Add new section
- id: post-sprint-create-feedback
  name: "Post-Sprint Creation Feedback"
  operation_type: command
  operation_pattern: "create-sprint"
  trigger_status: [success]
  feedback_config:
    questions:
      - "Sprint capacity: {total_points} points. Is this realistic?"
      - "You selected {story_count} stories. Confident in estimates?"
  enabled: false
```

**Step 2: Add Phase to Skill**

Edit `.claude/skills/devforgeai-orchestration/SKILL.md`:
- Add Phase 3.9 (Post-Sprint Feedback Hook) after Phase 3.8
- Follow Phase 4A.9 pattern (6 steps: check → parse → validate → invoke → monitor → handle errors)
- Update sprint mode workflow map

**Step 3: Update CLI (if needed)**

If sprint context requires new metadata extraction:
- Update `invoke_hooks.py` to read sprint files
- Extract sprint-specific metadata (capacity, story count, dates)
- Render questions with sprint placeholders

**Step 4: Create Tests**

```bash
# Unit tests
tests/unit/test_create_sprint_hooks.py

# Integration tests
tests/integration/test_create_sprint_hooks_e2e.py

# Performance tests
tests/performance/test_create_sprint_hooks_performance.py
```

**Step 5: Create Story**

```bash
/create-story "Wire hooks into /create-sprint command"
# Follow STORY-028 pattern for implementation
```

---

## Debugging Hook Issues

### Enable Debug Logging

**Temporary (one command):**
```bash
DEVFORGEAI_LOG_LEVEL=DEBUG /create-epic "Debug Epic"
```

**Persistent (configuration):**
```yaml
# Add to hooks.yaml
logging:
  level: DEBUG
  file: devforgeai/feedback/.logs/hooks-debug.log
```

**Debug Output Locations:**
- `devforgeai/feedback/.logs/hooks-debug.log`
- `devforgeai/feedback/.logs/hook-errors.log` (stack traces)

---

### Trace Hook Execution

**Add tracing to Phase 4A.9:**

```bash
# At start of each step
echo "[TRACE] Step 4A.9.1 starting" >> devforgeai/feedback/.logs/hooks-trace.log

# At decision points
echo "[TRACE] HOOKS_ENABLED=$HOOKS_ENABLED" >> devforgeai/feedback/.logs/hooks-trace.log

# At subprocess invocation
echo "[TRACE] Invoking: devforgeai invoke-hooks ..." >> devforgeai/feedback/.logs/hooks-trace.log
```

**Disable after debugging:**
- Comment out trace logging before commit
- Or wrap in `if [ "$DEBUG" = "true" ]; then ... fi`

---

### Reproduce Hook Failures

**Manual CLI Invocation:**

```bash
# Simulate Phase 4A.9.4 invocation
devforgeai invoke-hooks \
  --operation=epic-create \
  --epic-id=EPIC-001 \
  --timeout=30000

# Test with invalid inputs
devforgeai invoke-hooks --operation=epic-create --epic-id=EPIC-99999  # Should fail validation
devforgeai invoke-hooks --operation=epic-create --epic-id=invalid     # Should fail validation

# Test timeout behavior
devforgeai invoke-hooks --operation=epic-create --epic-id=EPIC-001 --timeout=1  # Should timeout immediately
```

**Mock Hook Failures:**

```python
# In test files
@patch('subprocess.run')
def test_hook_timeout(mock_run):
    # Simulate timeout (exit code 124)
    mock_run.return_value = subprocess.CompletedProcess(
        args=['devforgeai', 'invoke-hooks'],
        returncode=124,
        stdout='',
        stderr='Timed out after 30 seconds'
    )
    # Run Phase 4A.9
    # Assert: Epic creation exits 0, timeout logged
```

---

## Performance Optimization

### Baseline Metrics (STORY-028)

**Measured Performance:**
- Hook check: ~50-80ms (well under 100ms target)
- Hook invocation: ~200-400ms (well under 500ms target)
- Total overhead: ~500-1200ms (well under 3000ms target)

**Optimization Opportunities:**

1. **Configuration Caching**
   - Current: Loads hooks.yaml on each check-hooks invocation
   - Optimization: Cache parsed config in memory (invalidate on file change)
   - Benefit: Reduce check-hooks from 80ms → 10ms

2. **Lazy Epic File Loading**
   - Current: CLI reads epic file immediately
   - Optimization: Read only when rendering questions (defer until needed)
   - Benefit: Reduce invoke-hooks startup from 200ms → 100ms

3. **Async Logging**
   - Current: Synchronous log writes (blocking)
   - Optimization: Buffer logs, write async
   - Benefit: Reduce hook overhead from 500ms → 300ms

4. **Pre-compiled Regex**
   - Current: Regex compiled on each validation
   - Optimization: Compile once, reuse
   - Benefit: Minimal (regex compilation <1ms)

**Maintainer Action:** Measure before optimizing (use `time` command and profiling).

---

## Security Considerations

### Input Validation

**Epic ID Validation:**
```bash
# Regex: ^EPIC-[0-9]{3}$
# Allows: EPIC-001, EPIC-042, EPIC-999
# Blocks: EPIC-1, EPIC-9999, EPIC-ABC, epic-001, EPIC-001; rm -rf /
```

**Why This Matters:**
- Epic ID passed to shell subprocess: `devforgeai invoke-hooks --epic-id="$EPIC_ID"`
- Without validation: `--epic-id="EPIC-001; rm -rf /"` → command injection
- With validation: Malicious input rejected before CLI invocation

**Maintainer Note:** NEVER remove or weaken epic ID regex validation.

---

### Privilege Escalation Prevention

**Hook Execution Context:**
- Hooks run with same privileges as /create-epic command
- No sudo, no setuid, no privilege escalation
- User can only delete/modify files they already own

**File Permissions:**
- Log files: 644 (user read/write, group/others read-only)
- Feedback files: 600 (user read/write only, others no access)
- Configuration: 644 (readable by all users, writable by owner)

**Maintainer Action:**
```bash
# Set secure permissions on sensitive files
chmod 600 devforgeai/feedback/epic-create/*.json
chmod 644 devforgeai/config/hooks.yaml
chmod 644 devforgeai/feedback/.logs/*.log
```

---

### Secret Handling

**No Secrets in Hooks:**
- Epic metadata (features, complexity, risks) is NOT sensitive
- User feedback responses are personal, not secret
- No API keys, credentials, or tokens involved

**If Adding Secrets Later:**
- Use environment variables (never hardcode)
- Reference via ${SECRET_NAME} in configuration
- Document in hooks.yaml.example with placeholder values
- Add to .gitignore if secrets in local hooks.yaml

---

## Extending Hook System

### Add New Epic-Specific Question

**Edit hooks.yaml:**
```yaml
feedback_config:
  questions:
    - "You created {feature_count} features. Was this the right granularity?"
    - "NEW QUESTION: How confident are you in the timeline estimate?"  # Add here
```

**Add New Placeholder:**

If you want `{timeline_estimate}` placeholder:

1. Update CLI (`invoke_hooks.py`):
   ```python
   # Extract timeline from epic file
   timeline = extract_timeline_from_epic(epic_file)
   context['timeline_estimate'] = timeline
   ```

2. Update hooks.yaml.example documentation:
   ```yaml
   # Template placeholders supported:
   # - {feature_count} - Number of features
   # - {timeline_estimate} - Estimated duration (NEW)
   ```

3. Add unit test:
   ```python
   def test_extract_timeline_from_epic_context():
       assert extract_timeline("6 months") == "6 months"
   ```

---

### Add New Hook Operation

**Example: Add post-story-create hook**

1. **Define Configuration** (hooks.yaml.example):
   ```yaml
   - id: post-story-create-feedback
     operation_type: command
     operation_pattern: "create-story"
     trigger_status: [success]
   ```

2. **Add Phase to Skill** (devforgeai-story-creation):
   - Add Phase 8.1 (Post-Story Feedback Hook)
   - Follow Phase 4A.9 pattern

3. **Create Story:**
   ```bash
   /create-story "Wire hooks into /create-story command"
   # See STORY-027 for implementation
   ```

4. **Update This Guide:**
   - Add new section for story-create hooks
   - Document story-specific metadata extraction
   - Update hook lifecycle diagram

---

## Breaking Changes Protocol

### When CLI Signature Changes

**Example:** `invoke-hooks` adds required `--context-file` argument

**Impact Assessment:**
1. Check which skills invoke CLI (Grep: `invoke-hooks`)
2. Identify affected phases (e.g., Phase 4A.9.4)
3. Estimate update effort (lines changed × skills affected)

**Update Procedure:**
1. **Update CLI first** (backward compatible if possible)
2. **Update skills** (all phases invoking CLI)
3. **Update tests** (mock new signature)
4. **Update documentation** (this guide, troubleshooting)
5. **Version hooks.yaml** (bump format_version if schema changes)

**Communication:**
- Document in ADR (devforgeai/adrs/ADR-XXX-hook-cli-signature-change.md)
- Update CHANGELOG (devforgeai/CHANGELOG.md)
- Add migration guide (how to upgrade existing hooks)

---

### When Configuration Schema Changes

**Example:** Add new field `trigger_conditions.epic_type: ["feature", "tech-debt"]`

**Backward Compatibility:**
- Make new fields optional (provide defaults)
- Support old configuration (don't break existing hooks.yaml)
- Add migration script if breaking change unavoidable

**Migration Pattern:**
```bash
# migration script: migrate-hooks-config-v2.sh
#!/bin/bash
# Backup current config
cp hooks.yaml hooks.yaml.v1.backup

# Add new fields with defaults
sed -i 's/trigger_conditions:/trigger_conditions:\n    epic_type: ["feature", "tech-debt"]/' hooks.yaml

echo "Migration complete. Review hooks.yaml and test."
```

---

## Monitoring and Alerts

### Key Metrics

**Availability:**
- Hook system uptime: >99.9%
- CLI availability: 100% (local command, always available if installed)

**Performance:**
- Hook check latency p50/p95/p99: <50ms / <100ms / <150ms
- Hook invocation latency p50/p95/p99: <300ms / <500ms / <800ms
- Total overhead p50/p95/p99: <1s / <3s / <5s

**Reliability:**
- Hook success rate: >95%
- Hook timeout rate: <5%
- Epic creation success rate with hooks: >99.9% (NFR-003)

**Quality:**
- Feedback response rate: >50% (users answer vs skip)
- Feedback quality score: >3/5 (usefulness rating)

### Dashboard Queries

```bash
# Hook invocation count by operation
grep "Hook invoked" devforgeai/feedback/.logs/hooks.log | \
  grep "operation=" | \
  sed 's/.*operation=\([^ ]*\).*/\1/' | \
  sort | uniq -c | sort -rn

# Output:
#   42 epic-create
#   38 create-story
#   25 dev
#   12 qa

# Hook success rate (last 100 invocations)
success=$(tail -100 devforgeai/feedback/.logs/hooks.log | grep "exit_code=0" | wc -l)
echo "Success rate: $success% (last 100 hooks)"

# Average epic feature count (from feedback)
grep "feature_count" devforgeai/feedback/epic-create/*.json | \
  sed 's/.*: \([0-9]*\).*/\1/' | \
  awk '{sum+=$1; count++} END {print "Avg features: " sum/count}'
```

---

## Rollback Procedures

### Emergency Disable (Immediate)

```bash
# Option 1: Disable all hooks globally
echo "# Hooks disabled globally" > devforgeai/config/hooks.yaml

# Option 2: Disable epic-create hook only
sed -i 's/enabled: true/enabled: false/' devforgeai/config/hooks.yaml

# Option 3: Environment variable (one-time)
DEVFORGEAI_HOOKS_DISABLED=1 /create-epic "Emergency Epic"

# Verify
devforgeai check-hooks --operation=epic-create --status=success
# Should output: {"enabled": false, ...}
```

---

### Revert Implementation (Git)

```bash
# Find STORY-028 commit
git log --oneline --grep="STORY-028"

# Revert commit (creates new commit undoing changes)
git revert <commit-hash>

# Or reset to before implementation (destructive)
git reset --hard <commit-before-story-028>

# Verify epic creation works without hooks
/create-epic "Test Epic After Rollback"
```

---

### Rollback Checklist

After rollback:
- [ ] Epic creation works (test with /create-epic)
- [ ] No hook errors in logs
- [ ] Story status updated (mark STORY-028 as rolled back)
- [ ] Create RCA document (devforgeai/RCA/RCA-XXX-hook-rollback.md)
- [ ] Notify team (if multi-user project)
- [ ] Plan fix (create follow-up story if bug found)

---

## Future Enhancements

### Potential Improvements

1. **Adaptive Questions**
   - Ask different questions based on complexity score
   - Complex epics (≥7) get deeper questions
   - Simple epics (≤4) get basic questions

2. **Feedback Analytics**
   - Aggregate feedback across epics
   - Identify common pain points
   - Surface insights to product owners

3. **Multi-Language Support**
   - Questions in multiple languages (ES, FR, DE)
   - Configured per user preference
   - Translations in hooks.yaml or separate files

4. **Hook Chaining**
   - Epic-create hook triggers → Creates follow-up story hook
   - Dependencies between hooks
   - Conditional triggering based on previous feedback

5. **Batch Mode**
   - If creating 3 epics, prompt once vs 3 times
   - Configurable: `batch_mode: prompt_once` or `prompt_each`
   - Reduce feedback fatigue

---

## Maintenance Schedule

### Weekly Tasks
- [ ] Check hook error logs (any recurring failures?)
- [ ] Verify hook success rate >95%
- [ ] Review feedback response rate (users engaging?)

### Monthly Tasks
- [ ] Rotate log files (archive and compress)
- [ ] Analyze hook performance (check <100ms, invoke <500ms)
- [ ] Review feedback analytics (insights from epic feedback)
- [ ] Update hooks.yaml.example (new patterns discovered)

### Quarterly Tasks
- [ ] Review hook integration across all commands (dev, qa, release, epic, sprint, story)
- [ ] Optimize performance (if degraded)
- [ ] Security audit (input validation, logging)
- [ ] Update this maintainer guide (lessons learned, new patterns)

---

## Related Documentation

**Implementation:**
- `.claude/skills/devforgeai-orchestration/SKILL.md` (Phase 4A.9, lines 252-510)
- `.claude/commands/create-epic.md` (Phase 4 display logic)
- `devforgeai/config/hooks.yaml.example` (epic-create configuration, lines 87-152)

**Testing:**
- `tests/unit/test_create_epic_hooks.py` (37 unit tests)
- `tests/integration/test_create_epic_hooks_e2e.py` (12 integration tests)
- `tests/performance/test_create_epic_hooks_performance.py` (23 performance tests)
- `tests/STORY-028-*.md` (4 test documentation files)

**Troubleshooting:**
- `devforgeai/specs/STORY-028-TROUBLESHOOTING-GUIDE.md` (user-facing guide)

**Stories:**
- STORY-028: Wire Hooks Into /create-epic Command
- STORY-027: Wire Hooks Into /create-story Command (similar pattern)
- STORY-021: Implement devforgeai check-hooks CLI
- STORY-022: Implement devforgeai invoke-hooks CLI

**Framework:**
- EPIC-006: Feedback System Integration Completion
- `devforgeai/protocols/lean-orchestration-pattern.md` (command architecture)

---

## Contact and Support

**For Hook System Issues:**
- Check logs: `devforgeai/feedback/.logs/hook-errors.log`
- Review tests: `pytest tests/unit/test_create_epic_hooks.py -v`
- Consult troubleshooting guide: `devforgeai/specs/STORY-028-TROUBLESHOOTING-GUIDE.md`
- Create RCA if recurring: `devforgeai/RCA/RCA-XXX-hook-issue.md`

**For Feature Requests:**
- Create story: `/create-story "Enhance epic-create hook with [feature]"`
- Link to EPIC-006 (Feedback System Integration)
- Tag with "feedback-system", "hooks", "enhancement"

---

**Maintainer:** DevForgeAI Framework Team
**Last Updated:** 2025-11-16 (STORY-028 implementation)
**Next Review:** 2025-12-16 (1 month)
