# Parameter Extraction

## Overview

This skill cannot accept runtime parameters directly. All configuration is extracted from:
1. Conversation context (set by the `/setup-github-actions` command)
2. Existing configuration files
3. User responses to AskUserQuestion

## Extraction Algorithm

### Step 1: Extract Force Flag

Scan conversation context for `$FORCE_FLAG` or `--force` argument:

```
FORCE_FLAG = false

IF conversation contains "--force":
    FORCE_FLAG = true
IF conversation contains "$FORCE_FLAG = true":
    FORCE_FLAG = true
```

### Step 2: Load Existing Configuration

**Configuration Priority (highest to lowest):**
1. User-provided answers via AskUserQuestion (collected during Phase 02)
2. Values from existing `devforgeai/config/ci/github-actions.yaml`
3. Skill defaults

**Skill Defaults:**
```yaml
cost_optimization:
  enable_prompt_caching: true
  prefer_haiku: true
  max_cost_per_story: 0.15
  max_turns:
    simple: 10
    complex: 20
    architecture: 30

workflow:
  max_parallel_jobs: 5
  timeout_minutes: 30
  runner: ubuntu-latest

installer_testing:
  enabled: false
```

### Step 3: Merge Configuration

```
FOR each config_key in defaults:
    IF key exists in existing_config:
        merged[key] = existing_config[key]
    ELSE:
        merged[key] = defaults[key]

FOR each user_override in askuserquestion_responses:
    merged[override.key] = override.value
```

### Session ID Generation

Generate a unique session ID for this workflow execution:

```
SESSION_ID = "CI-{YYYY-MM-DD}-{NNN}"

Example: CI-2026-03-19-001
```

Where:
- `YYYY-MM-DD` is the current date
- `NNN` is a zero-padded sequence number (check existing state files to determine next number)
