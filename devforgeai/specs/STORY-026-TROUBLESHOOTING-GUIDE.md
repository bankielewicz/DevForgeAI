# STORY-026: Orchestrate Hooks Troubleshooting Guide

**Purpose:** Diagnose and resolve issues with orchestrate hook integration

**Scope:** Hook invocation, context extraction, configuration, and performance

**Created:** 2025-11-14

---

## Quick Diagnosis

### Symptom: Hook not triggering

**Check 1: Is hook enabled?**
```bash
grep -A 5 "post-orchestrate-retrospective" .devforgeai/config/hooks.yaml | grep "enabled"
# Expected: enabled: true
# If false: Set to true in hooks.yaml
```

**Check 2: Does workflow status match trigger?**
```bash
# If trigger_status: [failure] and workflow succeeded:
# Expected: Hook skipped (failures-only mode)
# Solution: This is correct behavior (AC4)

# If trigger_status: [failure] and workflow failed:
# Expected: Hook should trigger
# Solution: Check logs in next step
```

**Check 3: Check hook logs**
```bash
tail -50 .devforgeai/logs/hooks-orchestrate-{STORY-ID}.log
# Look for: Hook invocation attempt, exit codes, errors
```

---

### Symptom: Context extraction fails

**Check 1: Story file exists and readable**
```bash
ls -la devforgeai/specs/Stories/{STORY-ID}*.story.md
# Expected: File exists with read permissions
# If missing: Verify story ID correct
```

**Check 2: Story content valid**
```bash
# Validate YAML frontmatter
head -20 devforgeai/specs/Stories/{STORY-ID}*.story.md
# Expected: Valid YAML between ---  markers
# If invalid: Fix YAML syntax errors
```

**Check 3: Test context extraction manually**
```bash
python3 -c "
from devforgeai_cli.orchestrate_hooks import extract_orchestrate_context
import json

with open('devforgeai/specs/Stories/{STORY-ID}.story.md', 'r') as f:
    content = f.read()

context = extract_orchestrate_context(
    story_content=content,
    story_id='{STORY-ID}',
    workflow_start_time='2025-11-14T10:00:00Z'
)

print(json.dumps(context, indent=2))
"
# Expected: Valid JSON output with workflow context
# If error: Check Python traceback for details
```

---

### Symptom: Hook CLI not found

**Check 1: Is devforgeai CLI installed?**
```bash
which devforgeai
# Expected: /path/to/devforgeai

# If not found:
pip install --break-system-packages -e .claude/scripts/
```

**Check 2: Is check-hooks subcommand available?**
```bash
devforgeai check-hooks --help
# Expected: Usage information for check-hooks command
# If error: Reinstall CLI or check STORY-021 completion
```

**Check 3: Is invoke-hooks subcommand available?**
```bash
devforgeai invoke-hooks --help
# Expected: Usage information for invoke-hooks command
# If error: Check STORY-022 completion
```

---

### Symptom: Performance slow (>200ms overhead)

**Check 1: Measure hook check time**
```bash
time devforgeai check-hooks --operation=orchestrate --status=SUCCESS
# Expected: <100ms (p95)
# If slower: Check system load, disk I/O
```

**Check 2: Measure context extraction time**
```bash
time python3 -c "from devforgeai_cli.orchestrate_hooks import extract_orchestrate_context; ..."
# Expected: <50ms for typical story
# If slower: Check story file size, reduce content
```

**Check 3: Profile invocation**
```bash
# Add timing to /orchestrate.md Phase N
START=$(date +%s%N)
devforgeai check-hooks ...
END=$(date +%s%N)
DURATION=$(( ($END - $START) / 1000000 ))  # Convert to ms
echo "Hook check: ${DURATION}ms"
```

---

## Common Issues and Solutions

### Issue 1: Hook triggers on success when failures-only expected

**Cause:** `trigger_status` configured incorrectly in hooks.yaml

**Diagnosis:**
```bash
grep -A 3 "trigger_status" .devforgeai/config/hooks.yaml | grep orchestrate -A 3
# Check if: trigger_status: [success, failure]
```

**Solution:**
```yaml
# Change to failures-only mode (AC4 default):
trigger_status: [failure]  # NOT [success, failure]
```

**Verification:**
```bash
# Run successful workflow
/orchestrate STORY-XXX  # All phases pass
# Expected: "Hook not eligible (config: failures-only mode, workflow succeeded)"
```

---

### Issue 2: Checkpoint resume context missing

**Cause:** Story workflow history doesn't contain checkpoint information

**Diagnosis:**
```bash
# Check story file for Status History section
grep -A 50 "Status History" devforgeai/specs/Stories/{STORY-ID}.story.md

# Look for checkpoint entries like:
# | 2025-11-14 | Checkpoint: QA_APPROVED | Ready to resume from QA phase |
```

**Solution:**
```markdown
# Add checkpoint entry to story Status History:
| 2025-11-14 10:30 | Checkpoint: QA_APPROVED | QA complete, ready for release |
```

**Verification:**
```bash
# Extract context and check checkpoint_info field
python3 -c "from devforgeai_cli.orchestrate_hooks import extract_orchestrate_context; ..."
# Expected: "checkpoint_resumed": true, "resume_point": "QA_APPROVED"
```

---

### Issue 3: Quality gates not captured in context

**Cause:** QA Validation History section missing or incomplete

**Diagnosis:**
```bash
# Check story file for QA validation data
grep -A 20 "QA Validation History" devforgeai/specs/Stories/{STORY-ID}.story.md
```

**Solution:**
```markdown
# Add QA Validation History section to story:
## QA Validation History

### Validation 1 (2025-11-14 10:45)
- **Mode:** deep
- **Status:** PASSED
- **Coverage:** 87.5% (business: 95%, application: 85%, infrastructure: 82%)
- **Violations:** None
- **Deployment Verification:** All smoke tests passed
```

**Verification:**
```bash
# Extract context and check quality_gates field
# Expected: coverage_result, compliance_result, deployment_status all populated
```

---

### Issue 4: Workflow duration incorrect

**Cause:** workflow_start_time not set at /orchestrate workflow start

**Diagnosis:**
```bash
# Check if WORKFLOW_START_TIME variable is set in /orchestrate.md Phase 0
grep "WORKFLOW_START_TIME" .claude/commands/orchestrate.md
```

**Solution:**
```bash
# Add to /orchestrate.md Phase 0:
WORKFLOW_START_TIME=$(date -Iseconds)
export WORKFLOW_START_TIME

# Pass to context extraction in Phase N:
workflow_start_time='${WORKFLOW_START_TIME}'
```

**Verification:**
```bash
# Check context output
# Expected: "total_duration": 3600 (seconds), "start_time": "2025-11-14T10:00:00Z"
```

---

### Issue 5: Multiple QA retries not reflected in context

**Cause:** QA attempt count not tracked across retries

**Diagnosis:**
```bash
# Check story for multiple QA validation entries
grep -c "Validation [0-9]" devforgeai/specs/Stories/{STORY-ID}.story.md
# Expected: >1 if multiple attempts
```

**Solution:**
Story file should have multiple validation entries:
```markdown
## QA Validation History

### Validation 1 (2025-11-14 10:00)
- Status: FAILED
- Reason: Coverage below threshold

### Validation 2 (2025-11-14 11:00)
- Status: FAILED
- Reason: Anti-pattern violations

### Validation 3 (2025-11-14 12:00)
- Status: PASSED
```

**Verification:**
```bash
# Extract context
# Expected: "qa_attempts": 3, "qa_failure_reasons": ["Coverage below threshold", ...]
```

---

### Issue 6: Concurrent workflows creating race conditions

**Cause:** Log files or feedback files overwriting each other

**Diagnosis:**
```bash
# Check if multiple workflows running simultaneously
ps aux | grep orchestrate
# If multiple processes: Risk of race condition

# Check log file for conflicting entries
tail -50 .devforgeai/logs/hooks-orchestrate-*.log
# Look for: Interleaved entries from different stories
```

**Solution:**
Log files are already story-specific (AC: Edge Case 5):
```bash
# Each story gets its own log file:
.devforgeai/logs/hooks-orchestrate-STORY-001.log
.devforgeai/logs/hooks-orchestrate-STORY-002.log

# Feedback files include story ID and timestamp:
.devforgeai/feedback/orchestrate/STORY-001-20251114-120000.json
.devforgeai/feedback/orchestrate/STORY-002-20251114-120030.json
```

**Verification:**
```bash
# Run two workflows in parallel
/orchestrate STORY-001 &
/orchestrate STORY-002 &
wait

# Check separate log files exist
ls .devforgeai/logs/hooks-orchestrate-*.log
# Expected: Two files, no interleaving
```

---

### Issue 7: Hook invocation timeout

**Cause:** Feedback session taking >5 seconds to initialize

**Diagnosis:**
```bash
# Check hook invocation with timing
time devforgeai invoke-hooks --operation=orchestrate --story=STORY-XXX --context='...'
# If >5s: Timeout will occur
```

**Solution:**
```bash
# Add timeout wrapper in /orchestrate.md Phase N.4:
timeout 5s devforgeai invoke-hooks ... || {
  echo "⚠️ Feedback hook timed out (>5s), continuing..."
  # Log timeout
  echo "$(date): Hook timeout for $STORY_ID" >> .devforgeai/logs/hooks-orchestrate-${STORY_ID}.log
}
```

**Verification:**
```bash
# Simulate slow feedback (for testing)
# Expected: Timeout after 5s, workflow continues
```

---

### Issue 8: Invalid JSON in context

**Cause:** Story content contains unescaped quotes or special characters

**Diagnosis:**
```bash
# Test JSON validity
echo "$CONTEXT_JSON" | python3 -m json.tool
# If error: JSON is malformed
```

**Solution:**
```python
# Context extraction already handles JSON serialization
# If custom modifications made, ensure proper escaping:
import json
context_json = json.dumps(context)  # Handles escaping automatically
```

**Verification:**
```bash
# Validate extracted context
python3 -m json.tool < <(echo "$CONTEXT_JSON")
# Expected: Formatted JSON output, no errors
```

---

### Issue 9: Graceful degradation not working

**Cause:** Error handling missing in /orchestrate.md Phase N

**Diagnosis:**
Check if Phase N uses `|| { ... }` for error handling:
```bash
grep -A 5 "devforgeai invoke-hooks" .claude/commands/orchestrate.md
# Should have: || { echo "⚠️ ..."; }
```

**Solution:**
```bash
# Add error handling to all hook CLI calls:
devforgeai check-hooks ... 2>&1 || echo "⚠️ Hook check failed"
devforgeai invoke-hooks ... 2>&1 || echo "⚠️ Hook invocation failed"
```

**Verification:**
```bash
# Simulate hook failure (rename CLI temporarily)
mv $(which devforgeai) $(which devforgeai).bak
/orchestrate STORY-XXX
# Expected: Warning logged, workflow completes successfully

# Restore
mv $(which devforgeai).bak $(which devforgeai)
```

---

### Issue 10: Hooks.yaml changes not taking effect

**Cause:** Configuration not reloaded or cached

**Diagnosis:**
```bash
# Check file modification time
ls -l .devforgeai/config/hooks.yaml
# Verify changes are saved

# Check if CLI caches configuration
devforgeai check-hooks --version  # May show config cache info
```

**Solution:**
```bash
# Force reload (if CLI supports it)
# OR: Restart terminal/shell to clear any caches
```

**Verification:**
```bash
# Test hook with updated configuration
devforgeai check-hooks --operation=orchestrate --status=SUCCESS
# Should reflect latest hooks.yaml changes
```

---

## Debugging Tools

### Tool 1: Verbose Logging

```bash
# Enable debug logging in CLI
export DEVFORGEAI_LOG_LEVEL=DEBUG
devforgeai invoke-hooks ...
# Check detailed logs in .devforgeai/logs/
```

### Tool 2: Manual Context Extraction Test

```bash
# Create test script
cat > test_context_extraction.py <<'EOF'
from devforgeai_cli.orchestrate_hooks import extract_orchestrate_context
import json
import sys

if len(sys.argv) < 2:
    print("Usage: python test_context_extraction.py STORY-ID")
    sys.exit(1)

story_id = sys.argv[1]
story_file = f"devforgeai/specs/Stories/{story_id}.story.md"

try:
    with open(story_file, 'r') as f:
        content = f.read()

    context = extract_orchestrate_context(
        story_content=content,
        story_id=story_id,
        workflow_start_time='2025-11-14T10:00:00Z'
    )

    print(json.dumps(context, indent=2))
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)
EOF

# Run test
python test_context_extraction.py STORY-026
```

### Tool 3: Hook Configuration Validator

```bash
# Validate hooks.yaml syntax
python3 -c "
import yaml
with open('.devforgeai/config/hooks.yaml') as f:
    config = yaml.safe_load(f)
    print('✅ Valid YAML')
    print(f'Hooks defined: {len(config[\"hooks\"])}')
"
```

### Tool 4: Performance Profiler

```bash
# Profile context extraction
python3 -m cProfile -s cumtime -c "
from devforgeai_cli.orchestrate_hooks import extract_orchestrate_context
with open('devforgeai/specs/Stories/STORY-026.story.md') as f:
    content = f.read()
extract_orchestrate_context(content, 'STORY-026', '2025-11-14T10:00:00Z')
" 2>&1 | head -30
```

---

## Performance Optimization

### Optimization 1: Cache Story Content

```bash
# In /orchestrate.md, read story file once:
STORY_CONTENT=$(cat devforgeai/specs/Stories/${STORY_ID}*.story.md)

# Reuse in multiple places:
# - Context extraction
# - Status checking
# - Logging
```

### Optimization 2: Conditional Context Extraction

```bash
# Only extract context if hook is eligible:
if devforgeai check-hooks --operation=orchestrate --status=$OVERALL_STATUS; then
  # Hook eligible, extract full context
  CONTEXT_JSON=$(python3 -c "...")
else
  # Hook not eligible, skip extraction
  echo "Hook skipped, no context extraction needed"
fi
```

### Optimization 3: Use Binary CLI (Not Python Module)

```bash
# FAST (use installed CLI):
devforgeai check-hooks ...

# SLOW (don't use python -m):
python3 -m devforgeai_cli.commands.check_hooks ...
```

---

## Getting Help

### Internal Resources

- **Implementation:** `.claude/scripts/devforgeai_cli/orchestrate_hooks.py`
- **Tests:** `tests/unit/test_orchestrate_hooks_context_extraction.py` (31 tests)
- **Tests:** `tests/integration/test_orchestrate_hooks_integration.py` (56 tests)
- **Integration Guide:** `.devforgeai/specs/STORY-026-PHASE-N-INTEGRATION-PATTERN.md`
- **Config Example:** `.devforgeai/config/hooks.yaml.example`

### Log Files

- **Hook invocations:** `.devforgeai/logs/hooks-orchestrate-{STORY-ID}.log`
- **Feedback sessions:** `.devforgeai/feedback/orchestrate/{STORY-ID}-{timestamp}.json`
- **CLI errors:** `.devforgeai/logs/devforgeai-cli.log` (if logging configured)

### Test Validation

```bash
# Run all STORY-026 tests to verify implementation
pytest tests/unit/test_orchestrate_hooks_context_extraction.py \
       tests/integration/test_orchestrate_hooks_integration.py \
       -v

# Expected: 87/87 PASSED (100% pass rate)
```

---

**Last Updated:** 2025-11-14 (STORY-026 implementation)

**Related Stories:** STORY-021 (check-hooks CLI), STORY-022 (invoke-hooks CLI), STORY-023-025 (hook integration patterns)
