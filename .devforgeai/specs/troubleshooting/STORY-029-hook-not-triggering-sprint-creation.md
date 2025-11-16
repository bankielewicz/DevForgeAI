# Troubleshooting: Hook Not Triggering After Sprint Creation

**Issue:** Feedback hooks not triggering after `/create-sprint` command completion

**Story:** STORY-029 - Wire hooks into create-sprint command
**Component:** Phase N (Feedback Hook Integration)
**Severity:** LOW (non-blocking - sprint creation succeeds regardless)

---

## Symptoms

- Sprint file created successfully in `.ai_docs/Sprints/`
- Stories assigned to "Ready for Dev" status
- No feedback questions presented to user
- No feedback session file in `.devforgeai/feedback/`
- Command exits with code 0 (success)

---

## Resolution Steps

### Step 1: Verify Hooks Are Enabled in Configuration

**Check:** `.devforgeai/config/hooks.yaml`

```bash
# Read hook configuration
cat .devforgeai/config/hooks.yaml | grep -A 10 "post-sprint-create-feedback"
```

**Expected:**
```yaml
- id: post-sprint-create-feedback
  name: "Post-Sprint Creation Feedback"
  operation_pattern: "create-sprint"
  trigger_status: [success]
  enabled: true  # ← Must be true
```

**If enabled: false:**
```bash
# Enable hooks
sed -i 's/enabled: false/enabled: true/' .devforgeai/config/hooks.yaml

# Or manually edit .devforgeai/config/hooks.yaml
# Change: enabled: false → enabled: true
```

---

### Step 2: Verify DevForgeAI CLI Installed

**Check:** `devforgeai` command available

```bash
# Test CLI availability
which devforgeai
devforgeai --version
```

**If not found:**
```bash
# Install DevForgeAI CLI package
pip install --break-system-packages -e .claude/scripts/

# Verify installation
devforgeai --version
```

**Expected output:** `DevForgeAI CLI version X.Y.Z`

---

### Step 3: Test Hook Check Command Manually

**Run hook check command:**

```bash
# Test check-hooks (should return exit code 0 when enabled)
devforgeai check-hooks --operation=create-sprint --status=success
echo "Exit code: $?"
```

**Expected:**
- Exit code: 0 (hooks enabled)
- OR: "Hooks are disabled in configuration" with exit code 1

**If exit code 2 (invalid parameters):**
- Verify status parameter: Must be `success` (not `completed`, not `failed`)
- Verify operation parameter: Must be `create-sprint` exactly

---

### Step 4: Verify Phase N Exists in Command

**Check:** Phase N section in `.claude/commands/create-sprint.md`

```bash
# Search for Phase N
grep -n "Phase N" .claude/commands/create-sprint.md
```

**Expected:** Line 311 or similar (after Phase 4)

**If not found:**
```bash
# Re-implement STORY-029 or restore from git
git log --oneline | grep STORY-029
git show <commit-hash>:.claude/commands/create-sprint.md
```

---

### Step 5: Check Hook Configuration Syntax

**Validate YAML syntax:**

```bash
# Install yq if not available
# sudo apt-get install yq

# Validate YAML
python3 -c "import yaml; yaml.safe_load(open('.devforgeai/config/hooks.yaml'))"
```

**Expected:** No errors

**If syntax error:**
```bash
# Check error message for line number
python3 -c "import yaml; yaml.safe_load(open('.devforgeai/config/hooks.yaml'))" 2>&1

# Fix YAML syntax at indicated line
# Common issues: Missing quotes, wrong indentation, missing colons
```

---

### Step 6: Verify Log Files for Errors

**Check hook error log:**

```bash
# Read hook error log
cat .devforgeai/feedback/logs/hook-errors.log | tail -50
```

**Check command log:**

```bash
# Read command execution log
cat .devforgeai/logs/command.log | grep "Phase N" | tail -20
```

**Look for:**
- "Hook check returned non-zero, skipping invocation" (hooks disabled)
- "Hook invocation failed" (hook error occurred)
- "Timeout" or "Permission denied" (infrastructure issue)

---

### Step 7: Test Hook Invocation Manually

**Simulate hook invocation:**

```bash
# Test invoke-hooks command directly
devforgeai invoke-hooks \
  --operation=create-sprint \
  --sprint-name="Test-Sprint" \
  --story-count=5 \
  --capacity=25

echo "Exit code: $?"
```

**Expected:**
- Feedback questions presented
- Session file created in `.devforgeai/feedback/sessions/`
- Exit code: 0

**If error:**
- Check error message for root cause
- Verify feedback configuration in hooks.yaml
- Check Python dependencies installed

---

### Step 8: Check Terminal Restart

**Issue:** Command changes not loaded

**Solution:**
```bash
# Restart Claude Code Terminal
# (Commands are loaded at startup)

# Or reload commands dynamically (if supported)
# /reload
```

**After restart:**
- Phase N should be available
- Run `/create-sprint` again to test

---

### Step 9: Verify Trigger Conditions Met

**Check trigger conditions in hooks.yaml:**

```yaml
trigger_conditions:
  user_approval_required: false  # ← No manual approval needed
  operation_duration_min_ms: 0   # ← No minimum duration
  story_count_min: 3             # ← Example: Only if ≥3 stories selected
```

**If story_count_min: 3 but you selected 2 stories:**
- Hook won't trigger (condition not met)
- Remove or adjust `story_count_min` constraint
- Re-run `/create-sprint` with ≥3 stories

---

### Step 10: Review Hook Implementation in Phase N

**Verify Phase N implementation:**

```bash
# Read Phase N section
sed -n '311,333p' .claude/commands/create-sprint.md
```

**Expected structure:**
```markdown
### Phase N: Feedback Hook Integration

# Check hooks enabled
Execute: devforgeai check-hooks --operation=create-sprint --status=success

# Conditional invocation
IF check-hooks exit == 0:
    Execute: devforgeai invoke-hooks --operation=create-sprint \
      --sprint-name="${SPRINT_NAME}" \
      --story-count=${STORY_COUNT} \
      --capacity=${CAPACITY_POINTS}
```

**Verify:**
- [ ] `--operation=create-sprint` (correct operation)
- [ ] `--status=success` (correct status value)
- [ ] `--sprint-name="${SPRINT_NAME}"` (shell-escaped)
- [ ] `--story-count=${STORY_COUNT}` (integer)
- [ ] `--capacity=${CAPACITY_POINTS}` (integer)

---

## Common Issues & Solutions

### Issue 1: Exit Code 2 (Invalid Status Parameter)

**Error:** `devforgeai check-hooks: error: argument --status: invalid choice: 'completed'`

**Cause:** Status parameter must be `success`, `failure`, or `partial` (not `completed`)

**Solution:**
```bash
# Update Phase N in create-sprint.md
sed -i 's/--status=completed/--status=success/' .claude/commands/create-sprint.md

# Restart terminal to reload command
```

---

### Issue 2: Hooks Disabled in Config

**Log Message:** "Hooks are disabled in configuration"

**Cause:** `enabled: false` in hooks.yaml for post-sprint-create-feedback hook

**Solution:**
```bash
# Enable hooks
# Edit .devforgeai/config/hooks.yaml
# Find: enabled: false
# Change to: enabled: true

# Or use sed:
sed -i '/post-sprint-create-feedback/,/enabled:/ s/enabled: false/enabled: true/' .devforgeai/config/hooks.yaml
```

---

### Issue 3: Hook CLI Not Found

**Error:** `command not found: devforgeai`

**Cause:** DevForgeAI CLI package not installed

**Solution:**
```bash
# Install CLI package
pip install --break-system-packages -e .claude/scripts/

# Verify
devforgeai --version
```

---

### Issue 4: Sprint Context Variables Not Set

**Error:** Hook invocation missing parameters (empty --sprint-name, --story-count=0 when stories selected)

**Cause:** Variables not extracted correctly in Phase N

**Solution:**
```bash
# Verify variables set in Phase 3 (orchestration skill)
# SPRINT_NAME should be from user input or auto-generated
# STORY_COUNT should be from story selection count
# CAPACITY_POINTS should be sum of story points

# Check sprint-planner subagent result structure
```

---

### Issue 5: Trigger Condition Not Met

**Symptom:** Hook doesn't trigger for some sprint creations but does for others

**Cause:** Trigger conditions filter out certain sprints

**Check:**
```yaml
trigger_conditions:
  story_count_min: 5  # Only sprints with ≥5 stories
  capacity_min: 20    # Only sprints with ≥20 points
  epic_id: "EPIC-006" # Only sprints for specific epic
```

**Solution:**
- Remove restrictive conditions
- Or create sprint that meets conditions
- Or add multiple hook configurations for different scenarios

---

### Issue 6: Hook Timeout

**Error:** "Hook invocation timed out after 3000ms"

**Cause:** Feedback system hanging, network issues, or slow CLI initialization

**Solution:**
```bash
# Check timeout setting in hooks.yaml
max_duration_ms: 30000  # Increase if needed

# Test invoke-hooks performance
time devforgeai invoke-hooks --operation=create-sprint \
  --sprint-name="Test" --story-count=1 --capacity=5
```

---

### Issue 7: Permission Denied on Log Files

**Error:** "Permission denied: .devforgeai/feedback/logs/hook-errors.log"

**Cause:** Log directory or file has wrong permissions

**Solution:**
```bash
# Fix permissions
chmod 755 .devforgeai/feedback/logs/
chmod 644 .devforgeai/feedback/logs/*.log

# Or recreate log directory
rm -rf .devforgeai/feedback/logs/
mkdir -p .devforgeai/feedback/logs/
```

---

## Validation Checklist

**To confirm hook integration is working:**

- [ ] hooks.yaml exists with post-sprint-create-feedback configuration
- [ ] enabled: true in hook configuration
- [ ] devforgeai CLI installed and in PATH
- [ ] check-hooks returns exit code 0 when enabled
- [ ] Phase N exists in .claude/commands/create-sprint.md (lines 311-333)
- [ ] Sprint context variables set (SPRINT_NAME, STORY_COUNT, CAPACITY_POINTS)
- [ ] Trigger conditions met (story count, capacity, etc.)
- [ ] No YAML syntax errors in hooks.yaml
- [ ] Log directories exist with correct permissions
- [ ] Terminal restarted to load updated command

---

## Testing Hook Integration

**Manual test procedure:**

```bash
# 1. Enable hooks
sed -i '/post-sprint-create-feedback/,/enabled:/ s/enabled: false/enabled: true/' .devforgeai/config/hooks.yaml

# 2. Verify check-hooks
devforgeai check-hooks --operation=create-sprint --status=success
# Expected: Exit code 0

# 3. Run create-sprint
/create-sprint "Test-Hook-Sprint"
# Select 3 stories (15 points total)

# 4. Verify hook triggered
# Expected: Feedback questions presented after sprint creation
# Expected: Session file: .devforgeai/feedback/sessions/create-sprint-*.json

# 5. Verify sprint created
ls .ai_docs/Sprints/ | grep Test-Hook-Sprint
# Expected: Test-Hook-Sprint.md exists

# 6. Check logs
cat .devforgeai/logs/command.log | grep "Phase N"
# Expected: "Phase N: Checking feedback hooks for operation=create-sprint"
```

**Success Criteria:**
- Sprint file created ✓
- Hook invocation triggered ✓
- Feedback questions presented ✓
- Session file created ✓
- Command exit code 0 ✓

---

## Performance Diagnostics

**If hooks causing noticeable delay:**

```bash
# Measure check-hooks performance
time devforgeai check-hooks --operation=create-sprint --status=success

# Measure invoke-hooks performance
time devforgeai invoke-hooks --operation=create-sprint \
  --sprint-name="Perf-Test" --story-count=5 --capacity=25

# Targets:
# check-hooks: <100ms (NFR-001)
# invoke-hooks setup: <3s (NFR-002)
# Total Phase N: <3.5s (NFR-003)
```

**If exceeding targets:**
- Check CLI installation (should be pip-installed, not running via python -m)
- Check disk I/O (feedback files on slow storage?)
- Check Python dependencies (missing optimized libraries?)

---

## Related Documentation

- **Story:** `.ai_docs/Stories/STORY-029-wire-hooks-into-create-sprint-command.story.md`
- **Command:** `.claude/commands/create-sprint.md` (Phase N at lines 311-333)
- **Hook Config:** `.devforgeai/config/hooks.yaml` (post-sprint-create-feedback hook)
- **Hook Example:** `.devforgeai/config/hooks.yaml.example` (lines 155-221)
- **Sprint Planning Guide:** `.claude/skills/devforgeai-orchestration/references/sprint-planning-guide.md` (Hook Integration section)

---

## Support

**If issue persists after following all steps:**

1. Check DevForgeAI CLI logs: `.devforgeai/logs/cli.log`
2. Enable debug mode: `export DEVFORGEAI_DEBUG=1`
3. Re-run `/create-sprint` and capture full output
4. Review `.devforgeai/feedback/logs/hook-errors.log` for detailed errors
5. Consult framework maintainer or file GitHub issue

---

**Last Updated:** 2025-11-16 (STORY-029 implementation)
**Maintained By:** DevForgeAI Framework Team
