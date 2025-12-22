# Feedback System Migration Guide

Step-by-step guide to enabling automatic feedback on existing DevForgeAI projects.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step-by-Step Setup](#step-by-step-setup)
3. [Config File Locations and Defaults](#config-file-locations-and-defaults)
4. [Upgrade Path from Manual to Automatic](#upgrade-path-from-manual-to-automatic)
5. [Rollback Instructions](#rollback-instructions)

---

## Prerequisites

Before enabling automatic feedback, verify your project meets these requirements:

### Required Files

Check these files exist in your project:

```bash
# Verify config directory
ls devforgeai/config/

# Expected files:
# - feedback.yaml
# - hooks.yaml
# - feedback.schema.json (optional)
```

### Required Directories

```bash
# Verify feedback storage
ls devforgeai/feedback/

# Expected structure:
# - sessions/
# - feedback-index.json
```

### Create Missing Structure

If directories are missing:

```bash
# Create config directory
mkdir -p devforgeai/config

# Create feedback storage
mkdir -p devforgeai/feedback/sessions

# Initialize feedback index
echo '{"sessions": [], "version": "1.0"}' > devforgeai/feedback/feedback-index.json
```

### Version Requirements

- DevForgeAI Framework: 1.0+
- Claude Code Terminal: 1.0+
- Python (for CLI validators): 3.8+

---

## Step-by-Step Setup

### Step 1: Verify Config Files Exist

```bash
# Check for feedback.yaml
cat devforgeai/config/feedback.yaml
```

If missing, create with defaults:

```yaml
# devforgeai/config/feedback.yaml
enabled: true
trigger_mode: failures-only
operations:
  - qa
  - dev
conversation_settings:
  max_questions: 5
  allow_skip: true
skip_tracking:
  enabled: true
  max_consecutive_skips: 3
  reset_on_positive: true
templates:
  format: structured
  tone: brief
```

### Step 2: Create/Verify hooks.yaml

```bash
# Check for hooks.yaml
cat devforgeai/config/hooks.yaml
```

If missing, create with starter hooks:

```yaml
# devforgeai/config/hooks.yaml
hooks:
  - id: post-dev-feedback
    name: "Post-Development Feedback"
    operation_type: command
    operation_pattern: "dev"
    trigger_status: [success, partial]
    trigger_conditions:
      operation_duration_min_ms: 300000
      user_approval_required: true
    feedback_type: conversation
    feedback_config:
      mode: focused
    max_duration_ms: 5000
    enabled: true
    tags: [development, feedback]

  - id: post-qa-retrospective
    name: "Post-QA Retrospective"
    operation_type: command
    operation_pattern: "qa"
    trigger_status: [failure]
    feedback_type: conversation
    feedback_config:
      mode: focused
    max_duration_ms: 5000
    enabled: true
    tags: [qa, feedback]
```

### Step 3: Enable Hooks in feedback.yaml

Edit `devforgeai/config/feedback.yaml`:

```yaml
# Enable the master switch
enabled: true

# Choose trigger mode
trigger_mode: failures-only  # Start conservatively
```

### Step 4: Configure Trigger Mode

Choose based on your needs:

| Mode | Use When | Token Cost |
|------|----------|------------|
| `failures-only` | Production, minimal overhead | Low |
| `specific-operations` | Targeted feedback | Medium |
| `always` | Development/debugging | High |
| `never` | Disable completely | None |

### Step 5: Test with a Sample Operation

Run a quick test:

```bash
# Run a short operation
/qa STORY-001 light

# Check if feedback triggered (if it failed)
ls devforgeai/feedback/sessions/
```

### Step 6: Verify Configuration

```bash
# Run validation
devforgeai-validate check-hooks --operation=dev --status=success

# Expected output shows enabled hooks
```

---

## Config File Locations and Defaults

### Primary Configuration Files

| File | Location | Purpose |
|------|----------|---------|
| feedback.yaml | `devforgeai/config/feedback.yaml` | Master settings |
| hooks.yaml | `devforgeai/config/hooks.yaml` | Hook definitions |
| feedback.schema.json | `devforgeai/config/feedback.schema.json` | Validation schema |

### Storage Locations

| Type | Location | Purpose |
|------|----------|---------|
| Sessions | `devforgeai/feedback/sessions/` | Feedback data |
| Index | `devforgeai/feedback/feedback-index.json` | Session registry |

### Default Values

**feedback.yaml defaults:**

```yaml
enabled: true
trigger_mode: failures-only
conversation_settings:
  max_questions: 5
  allow_skip: true
skip_tracking:
  enabled: true
  max_consecutive_skips: 3
  reset_on_positive: true
templates:
  format: structured
  tone: brief
```

**Hook defaults:**

```yaml
max_duration_ms: 5000      # 5 seconds
enabled: true              # Active by default
feedback_type: conversation
```

---

## Upgrade Path from Manual to Automatic

If you've been using manual `/feedback` commands, follow this upgrade path:

### Step 1: Audit Current Usage

Review your manual feedback patterns:
- Which operations do you collect feedback for?
- What questions do you typically ask?
- How often do you collect feedback?

### Step 2: Map to Automatic Hooks

Create hooks matching your manual patterns:

**Before (Manual):**
```bash
/dev STORY-001
# ... development completes ...
/feedback  # Manual trigger
```

**After (Automatic):**
```yaml
# In hooks.yaml
- id: post-dev-feedback
  operation_pattern: "dev"
  trigger_status: [success, partial]
  enabled: true
```

### Step 3: Migrate Custom Questions

Move your common questions to hook configuration:

```yaml
feedback_config:
  mode: focused
  questions:
    - "Question from manual feedback 1?"
    - "Question from manual feedback 2?"
    - "Question from manual feedback 3?"
```

### Step 4: Gradual Rollout

Enable hooks progressively:

**Week 1:** Enable for failures only
```yaml
trigger_status: [failure]
```

**Week 2:** Add partial completions
```yaml
trigger_status: [failure, partial]
```

**Week 3:** Full coverage
```yaml
trigger_status: [success, failure, partial]
```

### Step 5: Retire Manual Commands

Once automatic hooks are working:
- Remove `/feedback` calls from workflows
- Update team documentation
- Archive manual feedback scripts

---

## Rollback Instructions

If you need to disable automatic feedback:

### Quick Disable (Master Switch)

```yaml
# In devforgeai/config/feedback.yaml
enabled: false  # Disables all hooks immediately
```

### Disable Specific Hooks

```yaml
# In devforgeai/config/hooks.yaml
- id: post-dev-feedback
  enabled: false  # Disable this hook only
```

### Complete Removal

To completely remove the feedback system:

```bash
# 1. Disable master switch
sed -i 's/enabled: true/enabled: false/' devforgeai/config/feedback.yaml

# 2. Backup and remove sessions (optional)
mv devforgeai/feedback/sessions devforgeai/feedback/sessions.backup

# 3. Disable all hooks
sed -i 's/enabled: true/enabled: false/g' devforgeai/config/hooks.yaml
```

### Restore from Rollback

To re-enable:

```bash
# 1. Enable master switch
sed -i 's/enabled: false/enabled: true/' devforgeai/config/feedback.yaml

# 2. Restore sessions (if backed up)
mv devforgeai/feedback/sessions.backup devforgeai/feedback/sessions

# 3. Enable desired hooks individually
# Edit devforgeai/config/hooks.yaml and set enabled: true
```

---

## Verification Checklist

After migration, verify:

- [ ] `devforgeai/config/feedback.yaml` exists with `enabled: true`
- [ ] `devforgeai/config/hooks.yaml` exists with at least one enabled hook
- [ ] `devforgeai/feedback/sessions/` directory exists
- [ ] `/audit-hooks` shows expected hooks enabled
- [ ] Test operation triggers feedback (or doesn't, per configuration)
- [ ] Feedback sessions are saved to `devforgeai/feedback/sessions/`

---

## Next Steps

- [User Guide](./feedback-system-user-guide.md) - Complete configuration reference
- [Troubleshooting](./feedback-troubleshooting.md) - Common issues and solutions
- [Architecture](../architecture/hook-system-design.md) - System design details
