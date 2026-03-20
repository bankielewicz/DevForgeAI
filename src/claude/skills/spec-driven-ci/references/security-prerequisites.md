# Security Prerequisites

## Required GitHub Secrets

All generated workflows require the following secrets to be configured in the GitHub repository before execution:

### ANTHROPIC_API_KEY (Required)

| Property | Value |
|----------|-------|
| Name | `ANTHROPIC_API_KEY` |
| Description | Claude API authentication key |
| Source | [console.anthropic.com](https://console.anthropic.com) |
| Required by | All 4 workflows |

**Setup Instructions:**

1. Navigate to repository **Settings > Secrets and variables > Actions**
2. Click **New repository secret**
3. Name: `ANTHROPIC_API_KEY`
4. Value: Your API key from console.anthropic.com
5. Click **Add secret**

### GITHUB_TOKEN (Automatic)

| Property | Value |
|----------|-------|
| Name | `GITHUB_TOKEN` |
| Description | Repository access token |
| Source | Automatically provided by GitHub Actions |
| Required by | qa-validation.yml (for PR comments) |

No setup required -- this token is automatically available in all GitHub Actions workflows.

## Fail-Fast Validation

All workflows include a validation step that checks for the API key before proceeding:

```yaml
- name: Validate API Key
  run: |
    if [ -z "${{ secrets.ANTHROPIC_API_KEY }}" ]; then
      echo "::error::ANTHROPIC_API_KEY secret not configured"
      echo "Setup: Repository Settings > Secrets > Actions > New repository secret"
      exit 1
    fi
```

This ensures workflows fail immediately with a clear error message rather than proceeding and failing mid-execution.

## Security Best Practices

1. **Never commit API keys** to the repository
   - Keys must be stored as GitHub Secrets
   - If a key is accidentally committed, rotate it immediately

2. **Use repository secrets** for sensitive values
   - Repository secrets are encrypted at rest
   - Secrets are masked in workflow logs
   - Secrets are only available to workflows in the repository

3. **Rotate keys periodically**
   - Rotate ANTHROPIC_API_KEY at least quarterly
   - Immediately rotate if team members leave

4. **Use environment protection rules** for production deployments
   - Create a "production" environment in GitHub
   - Require manual approval for production workflows
   - Limit which branches can deploy to production

5. **Audit secret access**
   - Review who has access to repository secrets
   - Use organization-level secrets for shared keys
   - Monitor API usage through console.anthropic.com

## Error Messages

| Condition | Error Message | Resolution |
|-----------|--------------|------------|
| Missing ANTHROPIC_API_KEY | "ANTHROPIC_API_KEY secret not configured" | Add secret in repo Settings |
| Invalid API key | "Authentication failed" | Verify key at console.anthropic.com |
| Expired API key | "API key expired" | Generate new key and update secret |
| Rate limited | "429 Too Many Requests" | Reduce max-parallel or add retry |

## Display During Skill Execution

Phase 01 and Phase 05 both display security information to the user:

**Phase 01 (Reminder):**
```
IMPORTANT: GitHub Actions workflows require ANTHROPIC_API_KEY as a GitHub Secret.
Setup: Repository Settings > Secrets and variables > Actions > New repository secret
```

**Phase 05 (Next Steps):**
```
NEXT STEPS - Required Before First Workflow Run:
1. Add ANTHROPIC_API_KEY to GitHub Secrets
2. Review ci-answers.yaml for headless prompts
3. Trigger your first workflow from the Actions tab
```
