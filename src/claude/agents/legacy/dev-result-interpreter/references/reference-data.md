# Reference Data

**Purpose:** Token budget, performance targets, output format details, and related subagents for the dev-result-interpreter subagent. Loaded via `Read()` from the Token Budget, Performance Targets, Output Format, and Related Subagents sections of the core agent file.

---

## Token Budget

**Haiku model (cost-effective):**
- Read story file: ~1.5K tokens
- Parse workflow and DoD status: ~2.5K tokens
- Extract test/quality metrics: ~2K tokens
- Generate display template: ~1.5K tokens
- Format output JSON: ~0.5K tokens
- **Total: <8K tokens per invocation**

**Optimization:**
- Single file read (story)
- No recursive file access
- Focused pattern matching
- Deterministic output format
- Parallel section extraction

---

## Performance Targets

- **Execution time:** <30 seconds
- **Token usage:** <8,000 tokens
- **Output size:** <6,000 characters
- **Accuracy:** 100% on story parsing, 99% on status inference

---

## Output Format

**Result Status Values:**
- `SUCCESS` - All TDD phases completed, all DoD items done, story status is Dev Complete
- `INCOMPLETE` - Workflow in progress, some phases/DoD items incomplete, story status is In Development
- `FAILURE` - Workflow error or inability to progress, status unchanged or rolled back

**Display Template Selection:**
- `dev_success_complete` - SUCCESS result
- `dev_incomplete_high_progress` - INCOMPLETE with 75%+ completion
- `dev_incomplete_moderate_progress` - INCOMPLETE with 50-75% completion
- `dev_incomplete_low_progress` - INCOMPLETE with <50% completion
- `dev_failure_with_error` - FAILURE with explicit error message
- `dev_failure_deferrals` - FAILURE caused by unresolved deferrals
- `dev_failure_no_progress` - FAILURE with no progress made

**Metrics Structure:**
- Workflow metrics: overall result, phases count, duration, success rate
- Implementation metrics: DoD items (completed/total), completion percentage
- Test metrics: test counts, pass rates, coverage by layer
- Code metrics: complexity, duplication, maintainability index
- Git metrics: commit hash, files changed, lines added/deleted

---

## Related Subagents

- **test-automator:** Generates tests; result-interpreter reports test counts and pass rates
- **backend-architect/frontend-developer:** Implement code; result-interpreter displays implementation status
- **code-reviewer:** Reviews code quality; result-interpreter displays quality metrics
- **deferral-validator:** Validates deferrals; result-interpreter displays deferral summary
- **qa-result-interpreter:** Receives dev-complete story from this subagent's workflow
