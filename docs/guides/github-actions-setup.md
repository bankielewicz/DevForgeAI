# GitHub Actions Setup Guide for DevForgeAI

Complete guide for setting up GitHub Actions CI/CD workflows with DevForgeAI.

## Overview

DevForgeAI provides GitHub Actions integration for headless execution of `/dev`, `/qa`, and parallel story development. This enables:

- Automated story implementation via CI/CD
- PR quality gates with QA validation
- Parallel story execution for team scaling
- Cost-optimized API usage (<$0.15/story)

## Prerequisites

### Required
- GitHub repository with DevForgeAI framework installed
- Anthropic API key from [console.anthropic.com](https://console.anthropic.com)
- DevForgeAI context files (`devforgeai/specs/context/*.md`)
- Git repository with commits

### Recommended
- GitHub Pro or Team (for environment protection rules)
- Existing stories in `devforgeai/specs/Stories/`

## Installation

### Option 1: Using /setup-github-actions Command (Recommended)

```bash
# Standard installation
/setup-github-actions

# Force overwrite existing files
/setup-github-actions --force
```

This command:
1. Validates Git repository status
2. Creates 4 workflow files in `.github/workflows/`
3. Creates 2 config files in `devforgeai/config/ci/`
4. Displays next steps for API key setup

### Option 2: Manual Installation

1. Copy workflow templates from `devforgeai/config/ci/` examples
2. Update configuration as needed
3. Add API key to repository secrets

## Configuration

### GitHub Secrets (Required)

Navigate to: Settings > Secrets and variables > Actions > New repository secret

| Secret Name | Description | Source |
|-------------|-------------|--------|
| `ANTHROPIC_API_KEY` | Claude API authentication | [console.anthropic.com](https://console.anthropic.com) |

**Note:** `GITHUB_TOKEN` is automatically provided by GitHub Actions.

### github-actions.yaml

Located at: `devforgeai/config/ci/github-actions.yaml`

```yaml
# Maximum parallel jobs (prevents API rate limit exhaustion)
max_parallel_jobs: 5

# Cost optimization settings
cost_optimization:
  enable_prompt_caching: true  # 90% cost savings
  prefer_haiku: true           # 3x cheaper model
  max_cost_per_story: 0.15     # USD threshold

# Rate limit handling
rate_limits:
  retry_on_429: true
  max_retries: 3
  backoff_seconds: [2, 4, 8]
```

### ci-answers.yaml

Located at: `devforgeai/config/ci/ci-answers.yaml`

Pre-configured answers for headless AskUserQuestion prompts:

```yaml
# What to do when tests fail during development
test_failure_action: fix-implementation  # Options: fix-implementation | fail-fast | retry-once

# Whether to allow deferrals in headless mode
deferral_strategy: never  # Options: never | with-approval | auto-approve

# Default priority for decisions
priority_default: high

# Technology choice when ambiguous
technology_choice: use_tech_stack_md
```

## Workflows

### 1. dev-story.yml - Story Development

**Purpose:** Execute `/dev` command headlessly for a single story.

**Trigger:** Manual (workflow_dispatch)

**Inputs:**
- `story_id` (required): Story identifier (e.g., "STORY-001")

**Usage:**
1. Go to Actions tab
2. Select "DevForgeAI Story Development"
3. Click "Run workflow"
4. Enter story ID
5. Click "Run workflow" button

**What happens:**
1. Validates story ID format (`STORY-NNN`)
2. Sets up Claude Code with cost optimization
3. Executes `/dev $story_id` in headless mode
4. Uploads artifacts (test results, coverage, story file)

**Artifacts:**
- `test-results-STORY-XXX`: Test output files
- `coverage-STORY-XXX`: Coverage reports
- `story-file-STORY-XXX`: Updated story file

### 2. qa-validation.yml - PR Quality Gate

**Purpose:** Automatically run QA validation on pull requests.

**Trigger:** Pull request to main branch (opened, synchronize)

**Requirements:**
- PR title must contain story ID: `[STORY-001] Description` or `STORY-001: Description`

**Behavior:**
1. Extracts story ID from PR title
2. Runs `/qa deep $story_id`
3. Posts results as PR comment
4. Blocks merge if QA fails

**Example PR titles:**
- `[STORY-001] Add user authentication`
- `STORY-042: Fix payment processing bug`
- `feat: STORY-007 implement dashboard`

### 3. parallel-stories.yml - Matrix Parallel Execution

**Purpose:** Execute multiple stories in parallel.

**Trigger:** Manual (workflow_dispatch)

**Inputs:**
- `story_ids` (required): JSON array of story IDs
  - Example: `["STORY-001", "STORY-002", "STORY-003"]`

**Configuration:**
- `max-parallel: 5` - Maximum concurrent jobs
- `fail-fast: false` - Continue other stories if one fails

**Usage:**
1. Go to Actions tab
2. Select "DevForgeAI Parallel Stories"
3. Enter story IDs as JSON array
4. Run workflow

**Considerations:**
- API rate limits: 50 RPM on Tier 1
- Cost: ~$0.12-0.15 per story
- Lock file coordination prevents commit conflicts

### 4. installer-testing.yml - Installer Tests

**Purpose:** Test installer package on changes.

**Trigger:** Push events modifying `installer/**`

**What it tests:**
- Package installation
- npm test suite
- Build verification

## Cost Management

### Cost Optimization Strategies

1. **Prompt Caching (90% savings)**
   - `CLAUDE_CODE_CACHE_ENABLED=true`
   - Framework context cached for 5 minutes

2. **Haiku Model (3x cheaper)**
   - `CLAUDE_CODE_MODEL=claude-haiku-4-5-20251001`
   - Sufficient for routine operations

3. **Turn Limits**
   - Simple stories: 10 turns
   - Complex stories: 20 turns
   - Architecture changes: 30 turns

### Cost Tracking

Each workflow run includes cost calculation:
- Extracted from Claude Code JSON output
- Logged to GitHub step summary
- Alert if exceeds `max_cost_per_story` threshold

### Estimated Costs

| Story Type | Estimated Cost |
|------------|----------------|
| Simple CRUD | $0.08-0.10 |
| Standard feature | $0.12-0.15 |
| Complex refactor | $0.15-0.20 |

## Security Best Practices

### API Key Protection
- Never commit API keys to repository
- Use GitHub repository secrets
- Rotate keys periodically

### Environment Protection
- Configure environment protection rules for production
- Require approvals for production deployments
- Enable required reviewers

### Secret Masking
- GitHub automatically masks secrets in logs
- Workflows validate secrets before execution
- Missing secrets fail fast with clear error

## Troubleshooting

### Common Issues

**"ANTHROPIC_API_KEY secret not configured"**
```
Solution: Add API key to repository secrets
Settings > Secrets > Actions > New repository secret
```

**"Story not found: STORY-XXX"**
```
Solution: Verify story file exists
Run: ls devforgeai/specs/Stories/STORY-XXX*
```

**"Rate limit exceeded (429)"**
```
Solution: Workflows include retry logic
If persistent: Reduce max_parallel_jobs in config
```

**"Workflow timeout (30 minutes)"**
```
Solution: Complex stories may timeout
Break into smaller stories or increase timeout
```

**"QA validation failed"**
```
Solution: Check QA report in PR comments
Common causes: Coverage below threshold, anti-pattern violations
```

### Debugging

Enable verbose logging:
```yaml
env:
  CLAUDE_CODE_DEBUG: true
```

Check workflow logs:
1. Go to Actions tab
2. Select failed workflow run
3. Click on failed job
4. Expand step with error

## Advanced Configuration

### Self-Hosted Runners

For private repositories or custom environments:

```yaml
# In github-actions.yaml
runners:
  default: self-hosted
  # Or with labels:
  # self_hosted: ["self-hosted", "linux", "x64"]
```

### Custom Workflow Triggers

Modify trigger conditions in workflow files:

```yaml
on:
  push:
    branches: [main, develop]
    paths: ['src/**', 'devforgeai/specs/Stories/**']
```

### Environment Variables

Available in all workflows:
- `CLAUDE_CODE_CACHE_ENABLED`: Enable prompt caching
- `CLAUDE_CODE_MODEL`: Override model selection
- `GITHUB_TOKEN`: Automatic repository access

## Related Documentation

- **Quick Reference:** `.github/README.md`
- **Skill Documentation:** `.claude/skills/devforgeai-github-actions/SKILL.md`
- **Configuration Examples:** `devforgeai/config/ci/*.example`
- **Story:** `devforgeai/specs/Stories/STORY-097-github-actions-workflow-templates.story.md`

## Version History

- **v1.0.0** (STORY-097): Initial implementation with 4 workflows, cost optimization, and headless mode support
