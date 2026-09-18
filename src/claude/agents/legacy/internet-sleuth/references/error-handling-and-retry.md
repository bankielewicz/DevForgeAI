# Error Handling and Retry Strategy for Internet Sleuth

**Version**: 1.0 | **Status**: Reference | **Agent**: internet-sleuth

---

## Error Handling Patterns

### Missing Context Files (Brownfield)

```
Error: Context validation failed
Missing files: devforgeai/specs/context/tech-stack.md, devforgeai/specs/context/dependencies.md

Action: Agent halts with structured error
Recommendation: Run /create-system-architecture command to generate missing context files before research
```

### Technology Conflict with tech-stack.md

```
Finding: Repository uses Vue.js for component architecture
Current tech-stack.md: React 18.2+

Action: Flag as "REQUIRES ADR - Proposed technology Vue.js conflicts with tech-stack.md specification React"
User Interaction:
  AskUserQuestion:
    - Option 1: Update tech-stack.md with ADR (create ADR-NNN-vue-js-evaluation.md)
    - Option 2: Adjust research scope to existing stack (analyze React patterns instead)
```

### Repository Access Denied (Authentication Required)

```
Error: Repository access denied (403)
Repository: https://github.com/private-org/private-repo

Action: Return structured error with remediation
Message: "Repository access denied. Manual authentication required. See GitHub CLI setup: https://cli.github.com/manual/gh_auth_login"
No retry attempts: Authentication errors are not transient
```

### GitHub API Rate Limit

```
Error: GitHub API rate limit exceeded (403)

Action: Retry with exponential backoff
Retry 1: Wait 1 second
Retry 2: Wait 2 seconds
Retry 3: Wait 4 seconds
Max retries: 3

If still failing: Continue with available repositories, note rate limit in summary
```

### Large Repository (>1000 files)

```
Warning: Repository has 5,243 files (token budget risk)

Action: Progressive disclosure approach
- Initial scan: README.md, package.json, src/ structure (10K tokens)
- Detailed analysis: High-value files only (configuration, main modules) (30K tokens max)
- Summary: Provide link to full repository for manual review
- Note: "Partial analysis due to repository size. See {repo-url} for complete codebase."
```

### Greenfield Project (No Context Files)

```
Info: Operating in greenfield mode - context files not yet created

Action: Proceed with research without constraint validation
Output: Include recommendations for initial tech-stack.md contents
Note in report: "Greenfield mode - context files should be created via /create-system-architecture before implementation"
```

### Invalid Repository URL

```
Error: Invalid repository URL
Provided: http://example.com/repo
Expected: https://github.com/{owner}/{repo} or git@github.com:{owner}/{repo}.git

Action: Return validation error with format specification
Message: "Invalid repository URL. Expected GitHub URL format: https://github.com/{owner}/{repo}"
```

---

## Retry Strategy

### GitHub API Failures

- **Max 3 retries:** 3 retry attempts with exponential backoff (max 3 retries total)
- **Backoff timing:** 1 second, 2 seconds, 4 seconds
- **Retry on transient failures:** Rate limits (429), network timeouts, 503 errors, 502 errors
- **Do NOT retry 401/403 errors:** 401 (unauthorized), 403 (forbidden - authentication required), 404 (not found) - these require user action, not retries

### Authentication Errors (Non-Transient)

- 401 Unauthorized: Missing or invalid credentials - return error immediately
- 403 Forbidden (auth): Requires authentication - return error with gh CLI setup instructions
- No retry attempts for authentication errors (not fixable without user intervention)

### Rationale

- Authentication failures require user action (providing GITHUB_TOKEN or running gh auth login)
- Retrying without credentials wastes time and API quota
- Transient failures (rate limits, network) benefit from retry with backoff

### Graceful Degradation

- If repository inaccessible (404, 403): Continue with available repositories
- Note failures in summary report: "Repository {name} inaccessible (404) - excluded from analysis"
- Provide partial results rather than complete failure

### Cleanup on Failure

- Use trap EXIT in Bash commands for guaranteed cleanup
- Example: `trap "rm -rf /tmp/spec-driven-research-$$" EXIT`
- Ensure temporary directories removed even if analysis fails mid-execution

### Error Structure

- Return structured JSON errors (not exceptions thrown to caller)
- Include: error type, remediation steps, affected repositories, partial results (if available)

---

## Staleness Detection Algorithm (Phase 1 Step 1.5)

```python
def check_staleness(report_date, report_state, current_date, current_state):
    workflow_states = ["Backlog", "Architecture", "Ready for Dev", "In Development",
                        "Dev Complete", "QA In Progress", "QA Approved", "QA Failed",
                        "Releasing", "Released"]

    age_days = (current_date - report_date).days
    state_distance = workflow_states.index(current_state) - workflow_states.index(report_state)

    if age_days > 30:
        return {"status": "STALE", "reason": f"Age: {age_days} days (threshold: 30)"}
    if state_distance >= 2:
        return {"status": "STALE", "reason": f"Workflow state distance: {state_distance} states (threshold: 2)"}

    return {"status": "CURRENT"}

# Example
report_date = "2025-10-01"
report_state = "Backlog"
current_date = "2025-11-17"  # 47 days later
current_state = "In Development"  # 2 states ahead

staleness = check_staleness(report_date, report_state, current_date, current_state)
# Returns: {"status": "STALE", "reason": "Age: 47 days (threshold: 30)"}
# AND: {"status": "STALE", "reason": "Workflow state distance: 2 states (threshold: 2)"}
```

**Action if STALE:**
- Flag report header: "⚠️ STALE RESEARCH (47 days old, 2 workflow states behind)"
- Recommend: "Re-research recommended with current workflow focus: [current focus]"
- Include in Section 6 (Workflow State) of report
