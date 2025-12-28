# Feedback System User Guide

> **See also:** [Feedback Overview](./feedback-overview.md) | [Troubleshooting](./feedback-troubleshooting.md) | [Migration Guide](./feedback-migration-guide.md)

Complete guide to configuring and using the DevForgeAI automatic feedback system.

## Table of Contents

1. [Introduction](#introduction)
2. [Enabling and Disabling Hooks](#enabling-and-disabling-hooks)
3. [Configuration Options](#configuration-options)
4. [Common Use Cases](#common-use-cases)
5. [Feedback Conversation Flow](#feedback-conversation-flow)

---

## Introduction

The DevForgeAI feedback system automatically collects insights after operations complete. It uses an event-driven hook architecture to trigger feedback conversations without modifying existing commands.

### What is the Feedback System?

The feedback system consists of:
- **Hooks** - Event triggers that fire when operations complete
- **Context Extraction** - Automatic analysis of operation outcomes
- **Adaptive Questions** - Context-aware questions based on what happened
- **Session Storage** - Persistent storage of feedback responses

### Benefits

- **Continuous Improvement** - Learn from successes and failures
- **Non-Invasive** - No changes to existing workflows required
- **Configurable** - Control when and how feedback is collected
- **Smart** - Questions adapt to operation context

---

## Enabling and Disabling Hooks

### Master Enable/Disable

Control all feedback with the master switch in `devforgeai/config/feedback.yaml`:

```yaml
# Enable all feedback
enabled: true

# Disable all feedback
enabled: false
```

### Per-Hook Control

Enable or disable individual hooks in `devforgeai/config/hooks.yaml`:

```yaml
hooks:
  - id: post-dev-feedback
    enabled: true   # This hook is active

  - id: post-qa-retrospective
    enabled: false  # This hook is inactive
```

### Checking Current Status

View enabled hooks:
```bash
/audit-hooks
```

Or inspect the configuration directly:
```bash
cat devforgeai/config/hooks.yaml | grep -A1 "id:"
```

---

## Configuration Options

### Trigger Modes

Control when feedback is collected in `devforgeai/config/feedback.yaml`:

```yaml
trigger_mode: failures-only
```

| Mode | Description | Recommended For |
|------|-------------|-----------------|
| `always` | Collect after every operation | Development/debugging |
| `failures-only` | Only on failures (default) | Production use |
| `specific-operations` | Only for listed operations | Targeted feedback |
| `never` | Disable all collection | When feedback not needed |

When using `specific-operations`, list the operations:

```yaml
trigger_mode: specific-operations
operations:
  - qa
  - dev
  - release
```

### Conversation Settings

Control the feedback interaction experience:

```yaml
conversation_settings:
  # Maximum questions per session (0 = unlimited)
  max_questions: 5

  # Allow skipping individual questions
  allow_skip: true
```

**Recommendations:**
- Set `max_questions: 5-7` to balance depth vs. user patience
- Keep `allow_skip: true` to prevent frustration

### Skip Tracking

Prevent feedback fatigue with skip tracking:

```yaml
skip_tracking:
  enabled: true
  max_consecutive_skips: 3    # Pause after 3 skips
  reset_on_positive: true     # Reset counter on engagement
```

When a user skips 3 consecutive feedback sessions, the system suggests:
> "You've skipped 3 feedback sessions. Would you like to disable automatic feedback?"

### Template Preferences

Control question format and tone:

```yaml
templates:
  format: structured    # structured or free-text
  tone: brief          # brief or detailed
```

| Format | Description |
|--------|-------------|
| `structured` | Multiple choice options (faster) |
| `free-text` | Open text input (more detailed) |

| Tone | Description |
|------|-------------|
| `brief` | Concise questions, no context |
| `detailed` | Full context with operation details |

---

## Common Use Cases

### Development Feedback After Long TDD Sessions

Collect insights after development work exceeding 5 minutes:

```yaml
# In hooks.yaml
- id: post-dev-feedback
  operation_type: command
  operation_pattern: "dev"
  trigger_status: [success, partial]
  trigger_conditions:
    operation_duration_min_ms: 300000  # 5 minutes
  enabled: true
```

**Sample questions:**
- "What challenges did you encounter during TDD?"
- "Were acceptance criteria clear and testable?"
- "Did you defer any DoD items? Why?"

### QA Retrospective on Failures

Learn from QA failures automatically:

```yaml
# In hooks.yaml
- id: post-qa-retrospective
  operation_type: command
  operation_pattern: "qa"
  trigger_status: [failure]
  trigger_conditions:
    result_code: partial  # With deferrals
  enabled: true
```

**Sample questions:**
- "Were QA failures expected or surprising?"
- "How can we prevent similar issues?"

### Custom Hook for Specific Operations

Create a hook for any operation:

```yaml
# In hooks.yaml
- id: my-custom-hook
  name: "Custom Operation Feedback"
  operation_type: command
  operation_pattern: "create-story"  # Or use glob: "create-*"
  trigger_status: [success]
  feedback_type: conversation
  feedback_config:
    mode: focused
    questions:
      - "Was the story specification clear?"
      - "Any suggestions for improvement?"
  max_duration_ms: 5000
  enabled: true
  tags: [custom, story-creation]
```

### Disable Feedback for Specific Commands

Use pattern exclusion:

```yaml
# In hooks.yaml
- id: exclude-ideate
  operation_pattern: "ideate"
  enabled: false  # Never trigger for /ideate
```

---

## Feedback Conversation Flow

### How Questions Are Selected

The adaptive questioning engine selects questions based on:

1. **Operation Type** - Different questions for dev vs. qa vs. release
2. **Outcome Status** - Success, failure, or partial completion
3. **Duration** - Long operations get different questions
4. **Error Context** - Failure details inform question selection

### Selection Logic

```
IF operation failed:
    → Use failure-focused questions
    → Include error context in questions
ELIF operation took > 10 minutes:
    → Use long-running operation questions
    → Ask about bottlenecks
ELSE:
    → Use standard success questions
    → Ask about improvements
```

### How Context Affects Questions

The system extracts context from TodoWrite state:

| Context | Question Adaptation |
|---------|---------------------|
| High error count | Focus on debugging experience |
| Many deferrals | Ask about blocking reasons |
| Long duration | Ask about performance concerns |
| Partial completion | Ask about remaining work |

### Skipping and Pause Behavior

Users can always skip questions:

1. **Individual Skip** - Skip current question, continue to next
2. **Session Skip** - Exit feedback session entirely
3. **Auto-Pause** - After 3 consecutive skips, system suggests disabling

**Skip Counter Reset:**
- Resets when user provides substantive feedback
- Resets at start of new day
- Does not count partial responses

### Example Conversation Flow

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DevForgeAI Feedback - Post-Development
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Operation: /dev STORY-042
Status: Success (12 minutes)
Phase: TDD Complete

Question 1/5:
What challenges did you encounter during TDD?

[ ] Test generation was difficult
[ ] Implementation took longer than expected
[ ] Acceptance criteria were unclear
[ ] Context file conflicts
[ ] No significant challenges
[ ] Other (specify)

> [User selects options]

Question 2/5:
The TDD Red phase took 4 minutes. Was this expected?

> [User responds]

...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Thank you for your feedback!
  Session saved to: devforgeai/feedback/sessions/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Next Steps

- [Architecture Documentation](../architecture/hook-system-design.md) - Understand system design
- [Troubleshooting Guide](./feedback-troubleshooting.md) - Solve common issues
- [Migration Guide](./feedback-migration-guide.md) - Enable on existing projects
