# DevForgeAI Feedback Skill

Automated feedback collection system with event-driven hooks for DevForgeAI operations.

## Quick Start

Enable automatic feedback in 3 steps:

### Step 1: Configure Trigger Mode

Edit `devforgeai/config/feedback.yaml`:

```yaml
enabled: true
trigger_mode: failures-only  # Options: always, failures-only, specific-operations, never
```

### Step 2: Enable Hook(s)

Edit `devforgeai/config/hooks.yaml` and set `enabled: true` for desired hooks:

```yaml
hooks:
  - id: post-dev-feedback
    enabled: true  # Enable this hook
```

### Step 3: Run an Operation

```bash
/dev STORY-001  # Feedback automatically triggers on completion
```

## Feature Overview

### Event-Driven Hooks
- **Automatic triggering** on operation completion (dev, qa, release, orchestrate)
- **Pattern matching** for flexible operation filtering (exact, glob, regex)
- **Condition-based** triggers (duration, status, token usage)
- **Timeout protection** prevents hanging operations

### Context Extraction
- **TaskList analysis** extracts operation context automatically
- **Phase detection** identifies completed workflow phases
- **Error capture** extracts failure details for targeted questions
- **Secret sanitization** removes sensitive data before feedback

### Adaptive Questioning
- **Context-aware** questions based on operation type and outcome
- **Duration-sensitive** different questions for long vs short operations
- **Failure-focused** targeted questions when operations fail
- **Fatigue prevention** skip tracking and question limits

## Configuration Quick Reference

### feedback.yaml

| Setting | Options | Default | Description |
|---------|---------|---------|-------------|
| `enabled` | true/false | true | Master enable/disable |
| `trigger_mode` | always, failures-only, specific-operations, never | failures-only | When to collect feedback |
| `max_questions` | 0-20 | 5 | Questions per session (0=unlimited) |
| `allow_skip` | true/false | true | Allow skipping questions |
| `max_consecutive_skips` | 1-10 | 3 | Skips before pausing |

### hooks.yaml

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique identifier (lowercase, hyphens) |
| `operation_type` | Yes | command, skill, or subagent |
| `operation_pattern` | Yes | Exact name, glob (*), or regex (^...$) |
| `trigger_status` | Yes | [success], [failure], or [success, failure] |
| `enabled` | No | Default: true |

## Directory Structure

```
.claude/skills/devforgeai-feedback/
├── README.md                              # This file
├── SKILL.md                               # Skill execution workflow (v2.0)
├── HOOK-SYSTEM.md                         # Complete hook system reference
├── references/
│   ├── adaptive-questioning.md            # Question selection logic
│   ├── context-extraction.md              # Context extraction patterns
│   ├── context-sanitization.md            # Secret/PII removal
│   ├── feedback-analysis-patterns.md      # Trend analysis patterns
│   ├── feedback-export-formats.md         # Export format specs
│   ├── feedback-persistence-guide.md      # Storage patterns
│   ├── feedback-question-templates.md     # Question templates
│   ├── feedback-search-help.md            # Search query help
│   ├── field-mapping-guide.md             # Template field mappings
│   ├── template-examples.md              # Sample templates
│   ├── template-format-specification.md   # Template YAML structure
│   ├── triage-workflow.md                 # Recommendation triage
│   └── user-customization-guide.md        # User config options
└── templates/
    ├── command-passed.yaml                # Successful command
    ├── command-failed.yaml                # Failed command
    ├── skill-passed.yaml                  # Successful skill
    ├── skill-failed.yaml                  # Failed skill
    ├── subagent-passed.yaml               # Successful subagent
    ├── subagent-failed.yaml               # Failed subagent
    └── generic.yaml                       # Fallback template
```

## Related Commands

| Command | Description |
|---------|-------------|
| `/feedback` | Manual feedback collection |
| `/feedback-config` | View/edit configuration |
| `/feedback-search` | Search feedback history |
| `/feedback-reindex` | Rebuild feedback index |
| `/feedback-export-data` | Export filtered data |
| `/export-feedback` | Export ZIP package |
| `/import-feedback` | Import ZIP package |
| `/recommendations-triage` | Process AI recommendations |
| `/audit-hooks` | Audit hook registry |

## Documentation

| Document | Description |
|----------|-------------|
| [HOOK-SYSTEM.md](./HOOK-SYSTEM.md) | Complete hook system technical reference |
| [SKILL.md](./SKILL.md) | Skill execution workflow |
