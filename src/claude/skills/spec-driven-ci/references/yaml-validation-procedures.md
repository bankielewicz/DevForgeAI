# YAML Validation Procedures

## Purpose

Validate all generated YAML files (workflows and configuration) for structural correctness before the skill completes. This ensures workflows will be accepted by GitHub Actions.

## Workflow File Validation

### Required Structure

Every GitHub Actions workflow YAML file must contain these top-level keys:

```yaml
name: <workflow name>          # Required: string
on: <trigger configuration>    # Required: object or string
jobs: <job definitions>        # Required: object
```

### Validation Checklist Per Workflow

| Check | What to Verify | Method |
|-------|---------------|--------|
| File exists | Path resolves to a file | `Glob(pattern="{file_path}")` |
| Non-empty | File has content | `Read()` returns content |
| Has `name:` | Top-level name key | `Grep(pattern="^name:", path="{file}")` |
| Has `on:` | Trigger configuration | `Grep(pattern="^on:", path="{file}")` |
| Has `jobs:` | Job definitions | `Grep(pattern="^jobs:", path="{file}")` |
| Has `steps:` | At least one job has steps | `Grep(pattern="steps:", path="{file}")` |

### Per-Template Validation

**dev-story.yml:**
- `workflow_dispatch` trigger with `story_id` input
- `CLAUDE_CODE_CACHE_ENABLED` in env
- `claude -p "/dev` in a run step
- `actions/upload-artifact` step present

**qa-validation.yml:**
- `pull_request` trigger on `[main]`
- Story ID extraction step
- `claude -p "/qa` in a run step
- `actions/github-script` step for PR comment

**parallel-stories.yml:**
- `workflow_dispatch` trigger with `story_ids` input
- `strategy.matrix` with `fromJSON`
- `max-parallel` configured
- `fail-fast: false`

**installer-testing.yml (if generated):**
- Trigger configuration present
- Installation step present
- Verification step present

## Configuration File Validation

### github-actions.yaml

| Check | What to Verify | Method |
|-------|---------------|--------|
| File exists | Path resolves | `Glob(pattern="devforgeai/config/ci/github-actions.yaml")` |
| Has cost_optimization | Section present | `Grep(pattern="cost_optimization:", path="{file}")` |
| Has enable_prompt_caching | Boolean value | `Grep(pattern="enable_prompt_caching:", path="{file}")` |
| Has prefer_haiku | Boolean value | `Grep(pattern="prefer_haiku:", path="{file}")` |
| Has max_turns | Section present | `Grep(pattern="max_turns:", path="{file}")` |

### ci-answers.yaml

| Check | What to Verify | Method |
|-------|---------------|--------|
| File exists | Path resolves | `Glob(pattern="devforgeai/config/ci/ci-answers.yaml")` |
| Has answers | Section present | `Grep(pattern="answers:", path="{file}")` |
| Has entries | At least 1 answer entry | `Grep(pattern="pattern:", path="{file}")` |

## Error Handling

If any validation check fails:

1. **Log the specific failure** - Which file, which check, what was found vs. expected
2. **Attempt auto-fix** - If the issue is a missing key, add it with the default value
3. **Re-validate** - Run the check again after the fix
4. **HALT on persistent failure** - If auto-fix fails, HALT and report the error

Do NOT skip validation and proceed. Invalid YAML will cause GitHub Actions to reject the workflow entirely.
