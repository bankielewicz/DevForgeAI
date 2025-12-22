# Feedback System Troubleshooting Guide

Solutions to common issues with the DevForgeAI feedback system.

## Table of Contents

1. [Common Issues](#common-issues)
2. [How to Check if Hooks are Enabled](#how-to-check-if-hooks-are-enabled)
3. [How to View Hook Invocation Logs](#how-to-view-hook-invocation-logs)
4. [FAQ](#faq)

---

## Common Issues

### Hooks Not Triggering

**Symptoms:** Feedback doesn't appear after operations complete.

**Possible Causes:**

1. **Master switch disabled**
   ```yaml
   # Check devforgeai/config/feedback.yaml
   enabled: false  # Should be true
   ```

2. **Hook disabled**
   ```yaml
   # Check devforgeai/config/hooks.yaml
   - id: post-dev-feedback
     enabled: false  # Should be true
   ```

3. **Pattern mismatch**
   ```yaml
   operation_pattern: "development"  # Won't match "dev"
   ```

4. **Trigger conditions not met**
   ```yaml
   trigger_conditions:
     operation_duration_min_ms: 300000  # 5 min - short ops won't trigger
   ```

5. **Status mismatch**
   ```yaml
   trigger_status: [failure]  # Won't trigger on success
   ```

**Solution:** Check each layer systematically:
```bash
# 1. Check master enable
grep "enabled:" devforgeai/config/feedback.yaml

# 2. Check hook enable
grep -A5 "id: post-dev" devforgeai/config/hooks.yaml

# 3. Verify pattern
grep "operation_pattern" devforgeai/config/hooks.yaml
```

---

### Context Extraction Failing

**Symptoms:** Questions seem generic or missing operation details.

**Possible Causes:**

1. **TodoWrite not updated** - Operation didn't update todos
2. **Timeout** - Extraction took too long (>200ms limit)
3. **Large todo count** - More than 150 todos triggers summarization

**Solution:**
```bash
# Check if context extraction module exists
ls -la src/context_extraction.py

# Verify TodoWrite was called in operation
# Look for TodoWrite calls in operation output
```

**Fallback Behavior:** When extraction fails, the system uses generic questions:
- "How did this operation go overall?"
- "What challenges did you encounter?"
- "Any suggestions for improvement?"

---

### Questions Seem Generic

**Symptoms:** Feedback questions don't reflect operation specifics.

**Possible Causes:**

1. **Context extraction returned empty**
2. **Operation type not recognized**
3. **Missing error context for failures**

**Solution:** Verify context is being extracted:
```bash
# Check adaptive questioning configuration
cat .claude/skills/devforgeai-feedback/references/adaptive-questioning.md

# Verify question templates exist
cat .claude/skills/devforgeai-feedback/references/feedback-question-templates.md
```

---

### Too Many Questions / Question Fatigue

**Symptoms:** Users feel overwhelmed by feedback requests.

**Solution:** Adjust conversation settings:
```yaml
# In devforgeai/config/feedback.yaml
conversation_settings:
  max_questions: 3        # Reduce from default 5
  allow_skip: true

skip_tracking:
  enabled: true
  max_consecutive_skips: 2  # Pause sooner
```

---

### Feedback Sessions Not Saved

**Symptoms:** Feedback responses lost after session.

**Possible Causes:**

1. **Write permission issue** on feedback directory
2. **Invalid session ID** format
3. **Storage path doesn't exist**

**Solution:**
```bash
# Check feedback directory exists and is writable
ls -la devforgeai/feedback/sessions/

# Create if missing
mkdir -p devforgeai/feedback/sessions/

# Check recent sessions
ls -lt devforgeai/feedback/sessions/ | head -5
```

---

## How to Check if Hooks are Enabled

### Method 1: Audit Command

```bash
/audit-hooks
```

Output shows enabled/disabled status for all hooks.

### Method 2: Direct Configuration Check

```bash
# Check master switch
grep "^enabled:" devforgeai/config/feedback.yaml

# Check individual hooks
grep -E "id:|enabled:" devforgeai/config/hooks.yaml
```

### Method 3: Programmatic Check

```python
# Using the CLI validator
devforgeai-validate check-hooks --operation=dev --status=success
```

### Expected Output (Hooks Enabled)

```
Hook Status Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Master: ENABLED
Trigger Mode: failures-only

Active Hooks:
  ✓ post-dev-feedback (command: dev)
  ✓ post-qa-retrospective (command: qa)

Disabled Hooks:
  ✗ post-release-monitoring
  ✗ sprint-retrospective
```

---

## How to View Hook Invocation Logs

### Method 1: Session Files

Feedback sessions are stored in:
```
devforgeai/feedback/sessions/
```

Each session file contains:
- Operation context
- Questions asked
- User responses
- Timestamps

### Method 2: Feedback Index

```bash
# View feedback index
cat devforgeai/feedback/feedback-index.json
```

### Method 3: Search Feedback History

```bash
/feedback-search --operation=dev --last=7d
```

### Log File Locations

| Log Type | Location |
|----------|----------|
| Session data | `devforgeai/feedback/sessions/*.json` |
| Session index | `devforgeai/feedback/feedback-index.json` |
| Hook config | `devforgeai/config/hooks.yaml` |
| Feedback config | `devforgeai/config/feedback.yaml` |

---

## FAQ

### FAQ 1: How do I completely disable feedback?

Set `enabled: false` in `devforgeai/config/feedback.yaml`:
```yaml
enabled: false
```

### FAQ 2: Can I have different settings for different operations?

Yes, create separate hooks with different configurations:
```yaml
hooks:
  - id: dev-quick-feedback
    operation_pattern: "dev"
    feedback_config:
      mode: focused
      questions: [...]

  - id: qa-detailed-feedback
    operation_pattern: "qa"
    feedback_config:
      mode: comprehensive
      questions: [...]
```

### FAQ 3: Why are my custom questions not appearing?

Ensure `feedback_config.questions` is properly formatted:
```yaml
feedback_config:
  mode: focused
  questions:
    - "First question?"      # Must be array format
    - "Second question?"
```

### FAQ 4: How do I add a new hook?

Add an entry to `devforgeai/config/hooks.yaml`:
```yaml
- id: my-new-hook
  name: "My New Hook"
  operation_type: command
  operation_pattern: "my-command"
  trigger_status: [success]
  feedback_type: conversation
  enabled: true
```

### FAQ 5: What's the difference between trigger_mode and trigger_status?

- **trigger_mode** (in feedback.yaml): Global setting for when to collect feedback
- **trigger_status** (in hooks.yaml): Per-hook setting for which outcomes trigger

### FAQ 6: How do I export feedback data?

```bash
/export-feedback --format=json --output=feedback-export.json
```

### FAQ 7: Can hooks trigger other hooks?

No, the circular dependency detector prevents this. Hooks cannot trigger other hooks to avoid infinite loops.

### FAQ 8: What happens if a hook times out?

The hook is gracefully terminated after `max_duration_ms` (default: 5000ms). The primary operation is not affected.

### FAQ 9: How do I reset skip tracking?

Delete the skip counter file or wait for the daily reset:
```bash
# Manual reset (if file exists)
rm devforgeai/feedback/.skip-counter
```

### FAQ 10: Can I use regex in operation_pattern?

Yes, use `^` and `$` anchors:
```yaml
operation_pattern: "^(dev|qa)$"  # Matches "dev" or "qa" exactly
```

### FAQ 11: How do I see what context was extracted?

Enable debug logging or check the session file:
```bash
cat devforgeai/feedback/sessions/latest.json | jq '.context'
```

### FAQ 12: Why does feedback trigger for short operations?

Check `operation_duration_min_ms` in trigger_conditions:
```yaml
trigger_conditions:
  operation_duration_min_ms: 60000  # Only >1 minute
```

---

## Getting Help

If these solutions don't resolve your issue:

1. **Check documentation:**
   - [User Guide](./feedback-system-user-guide.md)
   - [Architecture](../architecture/hook-system-design.md)

2. **Review configuration:**
   - `devforgeai/config/feedback.yaml`
   - `devforgeai/config/hooks.yaml`

3. **Check session data:**
   - `devforgeai/feedback/sessions/`

4. **Run validation:**
   ```bash
   devforgeai-validate check-hooks
   ```
