# STORY-028 Troubleshooting Guide: Hook Integration for /create-epic

**Purpose:** Resolve common issues with epic creation hooks (Phase 4A.9 feedback integration)

**Related:** STORY-028 (Wire Hooks Into /create-epic Command)

---

## Common Issues and Resolutions

### Issue 1: Hook Not Triggering After Epic Creation

**Symptom:** Epic created successfully, but no feedback prompt appears

**Diagnosis:**
```bash
# Check hook configuration
cat devforgeai/config/hooks.yaml | grep -A 10 "epic.create"

# Check if CLI is available
devforgeai check-hooks --operation=epic-create --status=success

# Check logs
tail -20 devforgeai/feedback/.logs/hooks.log
```

**Possible Causes & Solutions:**

1. **Hooks Disabled in Configuration**
   - **Cause:** `enabled: false` in hooks.yaml for epic-create operation
   - **Fix:** Edit `devforgeai/config/hooks.yaml`, set `enabled: true` for post-epic-create-feedback hook
   - **Verify:** Run `/create-epic` again, hook should trigger

2. **CLI Not Installed**
   - **Cause:** `devforgeai` command not found in PATH
   - **Fix:** Install CLI: `pip install --break-system-packages -e .claude/scripts/`
   - **Verify:** Run `devforgeai --version` (should show version number)

3. **Configuration File Missing**
   - **Cause:** `devforgeai/config/hooks.yaml` doesn't exist
   - **Fix:** Copy example: `cp devforgeai/config/hooks.yaml.example devforgeai/config/hooks.yaml`
   - **Edit:** Enable epic-create hook, set `enabled: true`
   - **Verify:** Run `devforgeai check-hooks --operation=epic-create --status=success`

4. **Wrong Trigger Status**
   - **Cause:** Hook configured for `trigger_status: [failure]` but epic succeeded
   - **Fix:** Change to `trigger_status: [success]` or `[success, failure]` in hooks.yaml
   - **Verify:** Check configuration matches expected trigger condition

---

### Issue 2: Hook Timeout (30-Second Limit Exceeded)

**Symptom:** Message appears: "Feedback hook timed out after 30s"

**Diagnosis:**
```bash
# Check timeout configuration
grep -A 5 "max_duration_ms" devforgeai/config/hooks.yaml

# Check hook logs for timeout entries
grep "timed out" devforgeai/feedback/.logs/hooks.log
```

**Possible Causes & Solutions:**

1. **Feedback Conversation Too Long**
   - **Cause:** User taking >30 seconds to answer questions
   - **Fix:** Increase timeout in hooks.yaml: `max_duration_ms: 60000` (60 seconds)
   - **Note:** Epic creation completes successfully even if hook times out (non-blocking)

2. **Network/Process Delay**
   - **Cause:** System slow, CLI startup overhead
   - **Fix:** Increase timeout buffer, optimize CLI installation
   - **Verify:** Run `time devforgeai invoke-hooks --operation=epic-create --epic-id=EPIC-001`

3. **Hook Script Hung**
   - **Cause:** Infinite loop or blocking I/O in feedback script
   - **Fix:** Timeout kills process automatically (SIGKILL after 30s)
   - **Action:** Review hook script for blocking operations
   - **Note:** Epic creation continues successfully (timeout is graceful)

---

### Issue 3: Hook CLI Error: "Invalid Epic ID Format"

**Symptom:** Error logged: "Invalid epic ID format: {epic-id}"

**Diagnosis:**
```bash
# Check epic ID in error log
grep "Invalid epic ID format" devforgeai/feedback/.logs/hook-errors.log

# Verify epic file exists
ls -la devforgeai/specs/Epics/EPIC-*.epic.md
```

**Possible Causes & Solutions:**

1. **Epic ID Doesn't Match EPIC-### Pattern**
   - **Cause:** Epic ID is EPIC-1 (should be EPIC-001) or EPIC-9999 (too many digits)
   - **Expected Format:** EPIC-XXX (exactly 3 digits: EPIC-001 through EPIC-999)
   - **Fix:** Rename epic file to match pattern
   - **Security Note:** Regex validation prevents command injection

2. **Epic ID Variable Not Set**
   - **Cause:** $EPIC_ID empty in Phase 4A.9.3
   - **Fix:** Verify Phase 4A.1 (Epic Discovery) sets EPIC_ID correctly
   - **Debug:** Add `echo "EPIC_ID=$EPIC_ID"` before Phase 4A.9.3

3. **Epic File Missing**
   - **Cause:** Epic file not created in Phase 4A.5
   - **Fix:** Verify Phase 4A.5 (Epic File Creation) completed successfully
   - **Debug:** Check `devforgeai/specs/Epics/` directory for epic file

---

### Issue 4: Hook Invocation Fails with "Epic File Not Found"

**Symptom:** Error: "Epic file not found" in hook-errors.log

**Diagnosis:**
```bash
# Verify epic file exists
ls -la devforgeai/specs/Epics/EPIC-*.epic.md

# Check file permissions
stat devforgeai/specs/Epics/EPIC-*.epic.md

# Check CLI can read epic file
devforgeai invoke-hooks --operation=epic-create --epic-id=EPIC-001 --dry-run
```

**Possible Causes & Solutions:**

1. **Epic File Path Incorrect**
   - **Expected Path:** `devforgeai/specs/Epics/EPIC-XXX-{slug}.epic.md`
   - **Cause:** File created in wrong directory (e.g., `devforgeai/epics/`)
   - **Fix:** Move epic file to correct location
   - **Verify:** Phase 4A.5 uses correct path per source-tree.md

2. **File Permissions Issue**
   - **Cause:** Epic file not readable by current user
   - **Fix:** `chmod 644 devforgeai/specs/Epics/EPIC-*.epic.md`
   - **Verify:** `cat devforgeai/specs/Epics/EPIC-*.epic.md` works

3. **Glob Pattern Not Matching**
   - **Cause:** Epic filename doesn't match EPIC-XXX-* pattern
   - **Fix:** Rename file to include slug: `EPIC-001-epic-name.epic.md`
   - **Standard:** Phase 4A.5 should create files with slug automatically

---

### Issue 5: Epic Context Metadata Incomplete

**Symptom:** Feedback questions don't reference epic details (generic questions instead of "{feature_count}")

**Diagnosis:**
```bash
# Check epic file has required metadata
grep -E "(features:|complexity:|risks:)" devforgeai/specs/Epics/EPIC-*.epic.md

# Check hook invocation logs
grep "metadata extraction" devforgeai/feedback/.logs/hooks.log
```

**Possible Causes & Solutions:**

1. **Epic File Missing Required Sections**
   - **Required:** Features list, Complexity score, Risks, Success criteria
   - **Fix:** Run Phase 4A.7 (Epic Validation) to detect missing sections
   - **Self-Heal:** Validation auto-adds default values if missing

2. **CLI Can't Parse Epic File**
   - **Cause:** Malformed YAML frontmatter or markdown structure
   - **Fix:** Validate epic file format against epic-template.md
   - **Verify:** `cat devforgeai/specs/Epics/EPIC-*.epic.md | head -50` (check frontmatter)

3. **Questions Not Customized**
   - **Cause:** Using default questions instead of epic-specific
   - **Fix:** Edit hooks.yaml questions array with {feature_count}, {complexity_score} placeholders
   - **Example:** See hooks.yaml.example lines 116-133

---

### Issue 6: Hook Fails But Epic Creation Also Fails

**Symptom:** Epic creation exits with non-zero code when hook fails

**Diagnosis:**
```bash
# Check last epic creation exit code
echo $?

# Check Phase 4A.9 error handling
grep "exit 0" .claude/skills/devforgeai-orchestration/SKILL.md | grep -A 5 "4A.9"
```

**Expected Behavior:** Epic creation ALWAYS exits 0 (hook failures are non-blocking)

**Possible Causes & Solutions:**

1. **Error Handling Not Implemented**
   - **Cause:** Phase 4A.9 missing `|| true` or proper error catching
   - **Fix:** Verify Step 4A.9.6 has comprehensive case statement
   - **Pattern:** All error paths should `return 0` or continue to Phase 4A.8

2. **Non-Blocking Pattern Violated**
   - **Cause:** Hook errors propagate to epic creation workflow
   - **Fix:** Wrap hook invocation: `devforgeai invoke-hooks ... || echo "Hook failed"`
   - **Verify:** Exit code is 0 even when hook crashes

3. **Validation Blocking Workflow**
   - **Cause:** Phase 4A.9.3 validation halts on missing epic file
   - **Fix:** Validation should skip hook (not halt epic creation)
   - **Pattern:** `if [ ! -f "$EPIC_FILE" ]; then return 0; fi`

---

### Issue 7: Performance Overhead >3 Seconds

**Symptom:** Epic creation takes significantly longer with hooks enabled

**Diagnosis:**
```bash
# Measure hook check performance
time devforgeai check-hooks --operation=epic-create --status=success

# Measure full hook overhead
# (Run /create-epic with hooks enabled vs disabled, compare duration)

# Check for bottlenecks
grep "duration" devforgeai/feedback/.logs/hooks.log
```

**Performance Targets:**
- Hook check: <100ms (p95)
- Hook invocation: <500ms (p95)
- Total overhead: <3000ms (p95)

**Possible Causes & Solutions:**

1. **CLI Startup Overhead**
   - **Cause:** Python interpreter startup on each invocation
   - **Fix:** Ensure CLI installed as executable (not `python -m`)
   - **Verify:** `which devforgeai` (should show /usr/local/bin or similar)

2. **Configuration File Too Large**
   - **Cause:** hooks.yaml has hundreds of hook definitions
   - **Fix:** Split into separate files or optimize YAML parsing
   - **Target:** <50 hook definitions per file

3. **Logging I/O Bottleneck**
   - **Cause:** Synchronous log writes on slow filesystem (network drive, WSL)
   - **Fix:** Use async logging or buffer writes
   - **Workaround:** Disable logging temporarily to verify if cause

4. **Hook Script Itself Slow**
   - **Cause:** Feedback CLI doing heavy processing (database queries, API calls)
   - **Fix:** Optimize feedback script, use caching
   - **Verify:** `time devforgeai invoke-hooks ...` (should complete in <500ms)

---

### Issue 8: Epic Creation Works But Feedback Not Saved

**Symptom:** Feedback conversation happens, but no file in `devforgeai/feedback/epic-create/`

**Diagnosis:**
```bash
# Check feedback directory structure
ls -la devforgeai/feedback/epic-create/

# Check feedback CLI logs
tail -50 devforgeai/feedback/.logs/feedback-cli.log

# Verify storage permissions
stat devforgeai/feedback/epic-create/
```

**Possible Causes & Solutions:**

1. **Directory Doesn't Exist**
   - **Cause:** `devforgeai/feedback/epic-create/` not created
   - **Fix:** `mkdir -p devforgeai/feedback/epic-create/`
   - **Auto-Fix:** CLI should create directory automatically

2. **Permission Denied**
   - **Cause:** Directory not writable by current user
   - **Fix:** `chmod 755 devforgeai/feedback/epic-create/`
   - **Verify:** `touch devforgeai/feedback/epic-create/test.txt`

3. **Storage Backend Misconfigured**
   - **Cause:** hooks.yaml specifies wrong storage path
   - **Fix:** Verify `storage_path` in feedback_config points to `devforgeai/feedback/epic-create/`
   - **Default:** If not specified, uses default path

4. **Feedback CLI Crash Before Save**
   - **Cause:** CLI crashes after conversation but before file write
   - **Fix:** Check `devforgeai/feedback/.logs/hook-errors.log` for stack trace
   - **Debug:** Run CLI manually to reproduce crash

---

### Issue 9: Multiple Hooks Triggering (Feedback Fatigue)

**Symptom:** User gets feedback prompts from dev, QA, release, AND epic-create hooks

**Diagnosis:**
```bash
# List all enabled hooks
grep "enabled: true" devforgeai/config/hooks.yaml

# Check hook invocation history
grep "Hook invoked" devforgeai/feedback/.logs/hooks.log | tail -20
```

**Possible Causes & Solutions:**

1. **All Hooks Enabled Simultaneously**
   - **Cause:** Every operation has hooks enabled
   - **Fix:** Disable some hooks based on team preference
   - **Strategy:** Enable only critical hooks (e.g., failures-only)

2. **No Trigger Filtering**
   - **Cause:** Hooks trigger on all statuses (success + failure)
   - **Fix:** Use `trigger_status: [failure]` for failures-only mode
   - **Example:** Only prompt when epic creation has issues

3. **Nested Command Hook Cascade**
   - **Cause:** /orchestrate calls /create-epic, both have hooks
   - **Expected:** Both hooks trigger (by design)
   - **Mitigation:** Use `trigger_conditions.operation_duration_min_ms` to skip quick operations

**Recommended Configuration:**
- Enable epic-create hooks for complex epics only (complexity_score_min: 6)
- Use failures-only mode for most hooks
- Limit hook count to 3-5 most valuable scenarios

---

### Issue 10: Hook Questions Don't Reference Epic Data

**Symptom:** Questions are generic ("Was the epic good?") instead of specific ("You created 5 features - was this right granularity?")

**Diagnosis:**
```bash
# Check if questions have placeholders
grep "{feature_count}" devforgeai/config/hooks.yaml

# Verify epic context passed to CLI
grep "epic-id=" devforgeai/feedback/.logs/hooks.log
```

**Possible Causes & Solutions:**

1. **Questions Missing Placeholders**
   - **Cause:** hooks.yaml questions don't use {feature_count}, {complexity_score} syntax
   - **Fix:** Update questions array in hooks.yaml
   - **Example:** `"You created {feature_count} features - was this the right granularity?"`
   - **See:** hooks.yaml.example lines 116-133 for proper format

2. **CLI Not Extracting Metadata**
   - **Cause:** devforgeai invoke-hooks not reading epic file
   - **Fix:** Verify CLI implementation reads `devforgeai/specs/Epics/{EPIC-ID}-*.epic.md`
   - **Debug:** Add logging in CLI to show extracted metadata

3. **Epic File Missing Metadata Sections**
   - **Cause:** Epic file doesn't have Features, Complexity, Risks sections
   - **Fix:** Run Phase 4A.7 (Epic Validation) to detect missing sections
   - **Self-Heal:** Validation auto-adds defaults if critical sections missing

**Template Placeholders Supported:**
- `{feature_count}` - Number of features (3-8 range)
- `{complexity_score}` - Complexity rating (0-10)
- `{risk_count}` - Number of risks identified
- `{epic_id}` - Epic identifier (EPIC-XXX)
- `{epic_name}` - Epic title/name

---

### Issue 11: Command Injection Warning in Logs

**Symptom:** Security warning: "Command injection attempt detected"

**Diagnosis:**
```bash
# Check security logs
grep "injection" devforgeai/feedback/.logs/hook-errors.log

# Verify epic ID format
ls devforgeai/specs/Epics/ | grep -v "^EPIC-[0-9]{3}"
```

**Possible Causes & Solutions:**

1. **Invalid Epic ID Format**
   - **Cause:** Epic ID is malformed (EPIC-99999, EPIC-ABC, epic-001)
   - **Expected:** EPIC-001 through EPIC-999 (exactly 3 digits, uppercase)
   - **Fix:** Rename epic file to match pattern
   - **Security:** Regex validation in Phase 4A.9.3 blocks invalid IDs

2. **Special Characters in Epic ID**
   - **Cause:** Epic ID contains shell metacharacters (; & | $ ` \)
   - **Protection:** Regex `^EPIC-[0-9]{3}$` allows only letters, hyphen, digits
   - **Action:** No fix needed - validation blocks automatically

3. **Epic ID from Untrusted Source**
   - **Cause:** Epic ID not generated by Phase 4A.1 (manual creation)
   - **Fix:** Always use /create-epic command (auto-generates valid IDs)
   - **Manual Creation:** If creating epics manually, follow EPIC-XXX format strictly

**Security Pattern:**
- Phase 4A.9.3 validates epic ID via regex BEFORE CLI invocation
- Variable passed with quotes: `--epic-id="$EPIC_ID"`
- No shell expansion possible (regex blocks special chars)

---

### Issue 12: Hook Invocation Succeeds But No Feedback Stored

**Symptom:** Hook executes, questions answered, but no file in feedback directory

**Diagnosis:**
```bash
# Check feedback index
cat devforgeai/feedback/feedback-index.json

# Check if session created
ls -la devforgeai/feedback/epic-create/

# Check CLI logs for storage errors
grep "storage" devforgeai/feedback/.logs/feedback-cli.log
```

**Possible Causes & Solutions:**

1. **Storage Path Misconfigured**
   - **Cause:** CLI saving to wrong directory
   - **Expected:** `devforgeai/feedback/epic-create/EPIC-XXX-{timestamp}.json`
   - **Fix:** Verify storage_path in hooks.yaml feedback_config
   - **Default:** Uses `devforgeai/feedback/{operation}/`

2. **Feedback Index Not Updated**
   - **Cause:** feedback-index.json not updated after session
   - **Fix:** Run `devforgeai feedback-reindex` to rebuild index
   - **Verify:** `devforgeai feedback-search "epic"` should list session

3. **Disk Space Exhausted**
   - **Cause:** No disk space available for writing files
   - **Fix:** `df -h devforgeai/feedback/` (check free space)
   - **Action:** Clean up old feedback files or increase disk space

4. **JSON Serialization Error**
   - **Cause:** Feedback responses contain invalid JSON characters
   - **Fix:** CLI should sanitize responses before saving
   - **Debug:** Check hook-errors.log for "serialization" errors

---

### Issue 13: Hooks Work in /create-epic But Not in /orchestrate

**Symptom:** Hooks trigger when running `/create-epic` directly, but not when epic created via `/orchestrate`

**Diagnosis:**
```bash
# Verify /orchestrate invokes devforgeai-orchestration skill
grep "devforgeai-orchestration" .claude/commands/orchestrate.md

# Check if orchestrate mode detects epic creation
grep "create-epic" .claude/skills/devforgeai-orchestration/SKILL.md
```

**Possible Causes & Solutions:**

1. **Orchestration Skill Doesn't Invoke Phase 4A**
   - **Cause:** /orchestrate doesn't trigger epic creation mode
   - **Expected:** /orchestrate is for story lifecycle, not epic creation
   - **Clarification:** Epics are created via /create-epic ONLY (not /orchestrate)
   - **No Fix Needed:** This is expected behavior

2. **Mode Detection Incorrect**
   - **Cause:** Skill mode detection doesn't recognize epic creation from /orchestrate
   - **Fix:** N/A - /orchestrate doesn't create epics
   - **Use Case:** Use /create-epic for epics, /orchestrate for story execution

**Expected Behavior:**
- `/create-epic` → devforgeai-orchestration (epic mode) → Phase 4A.9 → hooks trigger ✓
- `/orchestrate STORY-XXX` → devforgeai-orchestration (story mode) → No epic creation → No epic hooks ✓

---

## Quick Diagnostic Commands

### Check Hook System Health

```bash
# 1. Verify CLI installed
devforgeai --version

# 2. Check configuration
cat devforgeai/config/hooks.yaml | grep -A 20 "epic.create"

# 3. Test hook check (should be <100ms)
time devforgeai check-hooks --operation=epic-create --status=success

# 4. Check recent hook invocations
tail -20 devforgeai/feedback/.logs/hooks.log

# 5. Check for errors
tail -20 devforgeai/feedback/.logs/hook-errors.log

# 6. Verify feedback storage
ls -la devforgeai/feedback/epic-create/
```

### Enable Epic Create Hooks

```bash
# 1. Copy example configuration
cp devforgeai/config/hooks.yaml.example devforgeai/config/hooks.yaml

# 2. Enable epic-create hook
# Edit devforgeai/config/hooks.yaml:
#   Find "post-epic-create-feedback" section
#   Change: enabled: false → enabled: true

# 3. Verify
devforgeai check-hooks --operation=epic-create --status=success
# Should output: {"enabled": true, "available": true, ...}

# 4. Test with epic creation
/create-epic "Test Epic for Hook Validation"
# Should trigger feedback prompt after epic created
```

### Disable Hooks Temporarily

```bash
# Option 1: Edit hooks.yaml (persistent)
# Set enabled: false for epic-create hook

# Option 2: Environment variable (temporary, one command)
DEVFORGEAI_HOOKS_DISABLED=1 /create-epic "No Hooks Epic"

# Option 3: Delete hooks.yaml (all hooks disabled)
mv devforgeai/config/hooks.yaml devforgeai/config/hooks.yaml.disabled
```

---

## Logging Best Practices

### Log Locations

- **Success logs:** `devforgeai/feedback/.logs/hooks.log`
- **Error logs:** `devforgeai/feedback/.logs/hook-errors.log`
- **Feedback sessions:** `devforgeai/feedback/epic-create/EPIC-XXX-{timestamp}.json`

### Log Retention

```bash
# Archive old logs (monthly)
tar -czf hooks-archive-$(date +%Y-%m).tar.gz devforgeai/feedback/.logs/*.log
mv devforgeai/feedback/.logs/*.log devforgeai/feedback/.archives/

# Rotate logs when >10MB
find devforgeai/feedback/.logs/ -name "*.log" -size +10M -exec mv {} {}.old \;
```

### Log Analysis

```bash
# Count hook invocations per operation
grep "Hook invoked" devforgeai/feedback/.logs/hooks.log | cut -d' ' -f5 | sort | uniq -c

# Calculate average hook duration
grep "duration=" devforgeai/feedback/.logs/hooks.log | sed 's/.*duration=\([0-9]*\)ms.*/\1/' | awk '{sum+=$1; count++} END {print sum/count " ms"}'

# Find hook failures
grep "ERROR" devforgeai/feedback/.logs/hook-errors.log

# Check hook timeout rate
grep "timed out" devforgeai/feedback/.logs/hooks.log | wc -l
```

---

## Configuration Reference

### Minimal Epic Create Hook Configuration

```yaml
# Add to devforgeai/config/hooks.yaml

- id: post-epic-create-feedback
  name: "Post-Epic Creation Feedback"
  operation_type: command
  operation_pattern: "create-epic"
  trigger_status: [success]
  trigger_conditions:
    user_approval_required: false
  feedback_type: conversation
  feedback_config:
    mode: "focused"
    questions:
      - "You created {feature_count} features. Was this the right granularity?"
      - "Complexity score: {complexity_score}/10. Confident in this assessment?"
  max_duration_ms: 30000
  enabled: true  # Set to true to enable
```

### Advanced Configuration (With Filtering)

```yaml
- id: complex-epic-feedback
  name: "Complex Epic Feedback Only"
  operation_type: command
  operation_pattern: "create-epic"
  trigger_status: [success]
  trigger_conditions:
    # Only trigger for complex epics
    complexity_score_min: 7
    feature_count_min: 5
  feedback_config:
    questions:
      - "This is a complex epic ({complexity_score}/10). Any concerns?"
      - "With {feature_count} features, how confident in estimates?"
  enabled: true
```

---

## Related Documentation

**Implementation:**
- `.claude/skills/devforgeai-orchestration/SKILL.md` (Phase 4A.9, lines 252-510)
- `devforgeai/config/hooks.yaml.example` (lines 87-152)

**Testing:**
- `tests/unit/test_create_epic_hooks.py` (37 unit tests)
- `tests/integration/test_create_epic_hooks_e2e.py` (12 integration tests)
- `tests/performance/test_create_epic_hooks_performance.py` (23 performance tests)

**Stories:**
- STORY-028: Wire Hooks Into /create-epic Command (this story)
- STORY-021: Implement devforgeai check-hooks CLI command
- STORY-022: Implement devforgeai invoke-hooks CLI command
- STORY-027: Wire Hooks Into /create-story Command (similar pattern)

**Framework:**
- EPIC-006: Feedback System Integration Completion

---

## Emergency Rollback

If hook integration causes critical issues:

```bash
# 1. Disable all hooks immediately
echo "# All hooks disabled" > devforgeai/config/hooks.yaml

# 2. Or revert Phase 4A.9 implementation
git revert HEAD  # Reverts STORY-028 commit

# 3. Verify epic creation works without hooks
/create-epic "Test Epic Without Hooks"

# 4. Report issue for investigation
# Create incident report in devforgeai/RCA/
```

---

## Support

**For issues not covered in this guide:**
1. Check `devforgeai/feedback/.logs/hook-errors.log` for detailed error messages
2. Run `/audit-budget` to verify command budget compliance
3. Review STORY-028 test suite for expected behavior examples
4. Create RCA document if recurring issue found

**Last Updated:** 2025-11-16 (STORY-028 implementation)
