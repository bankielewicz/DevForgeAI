# Cost Optimization Strategies

## Token Pricing Reference (as of 2025)

| Model | Input Tokens | Output Tokens |
|-------|--------------|---------------|
| Claude Opus 4.5 | $15/MTok | $75/MTok |
| Claude Haiku 4.5 | $0.25/MTok | $1.25/MTok |

**Key insight:** Haiku is 60x cheaper for both input and output tokens.

## Typical Story Cost Breakdown

```
Story: STORY-001 (Simple CRUD feature)

Context loading:     ~50K tokens (input)
Conversation:        ~20K tokens (output)
Total tokens:        ~70K tokens

Without optimization (Opus):
  (50K x $15 + 20K x $75) / 1M = $2.25

With optimization (Haiku + Cache):
  (50K x $0.25 + 20K x $1.25) / 1M = $0.0375
  With 90% caching: $0.00375 + $0.025 = $0.03

Savings: 98.7% ($2.25 -> $0.03)
```

---

## Strategy 1: Prompt Caching (90% Savings)

Enable caching to reuse framework context across turns:

```yaml
env:
  CLAUDE_CODE_CACHE_ENABLED: true
```

**What gets cached:**
- CLAUDE.md project instructions
- Context files (tech-stack.md, source-tree.md, etc.)
- Skill SKILL.md content
- Story file content (after initial load)

**Cache duration:** 5 minutes
**Break-even:** 2+ turns per story (almost always met)

### Verification

Check all workflow files contain:
```
Grep(pattern="CLAUDE_CODE_CACHE_ENABLED: true", path=".github/workflows/")
```

---

## Strategy 2: Haiku Model (60x Cheaper)

Use Haiku for routine operations:

```yaml
env:
  CLAUDE_CODE_MODEL: claude-opus-4-6
```

**When Haiku is sufficient:**
- Test generation (TDD Red phase)
- Code implementation (TDD Green phase)
- File operations and refactoring
- QA validation (pattern matching)

**When Opus may be needed:**
- Complex architectural decisions
- Novel problem solving
- Multi-file refactoring with dependencies
- Security-sensitive implementations

### Verification

Check model preference is applied:
```
Grep(pattern="CLAUDE_CODE_MODEL", path=".github/workflows/")
```

---

## Strategy 3: Turn Limits

Prevent runaway costs with configurable turn limits:

```yaml
cost_optimization:
  max_turns:
    simple: 10      # Simple CRUD stories
    complex: 20     # Standard implementations
    architecture: 30 # Major refactoring
```

### Verification

Check github-actions.yaml contains max_turns section:
```
Grep(pattern="max_turns", path="devforgeai/config/ci/github-actions.yaml")
```

---

## Strategy 4: Early Termination

Stop workflows that exceed budget:

```yaml
- name: Check Cost
  run: |
    COST=$(jq -r '.total_cost_usd // 0' dev-result.json)
    if (( $(echo "$COST > 0.15" | bc -l) )); then
      echo "::error::Cost exceeded threshold: $$COST"
      exit 1
    fi
```

---

## Cost Monitoring

### Per-Workflow Tracking

```yaml
- name: Log Cost Summary
  run: |
    COST=$(jq -r '.total_cost_usd // 0' dev-result.json)
    echo "### Cost Summary" >> $GITHUB_STEP_SUMMARY
    echo "- Story: ${{ inputs.story_id }}" >> $GITHUB_STEP_SUMMARY
    echo "- Cost: \$$COST" >> $GITHUB_STEP_SUMMARY
    echo "- Model: ${CLAUDE_CODE_MODEL:-default}" >> $GITHUB_STEP_SUMMARY
```

### Monthly Budget Estimates

| Stories/Month | Without Optimization | With Optimization |
|---------------|---------------------|-------------------|
| 10 | $22.50 | $0.30 |
| 50 | $112.50 | $1.50 |
| 100 | $225.00 | $3.00 |

### Cost Alerts

Configure GitHub Actions budget alerts:
1. Go to Settings > Billing
2. Set spending limit
3. Enable email notifications

---

## Best Practices

### 1. Right-Size Stories

| Story Size | Points | Expected Cost |
|------------|--------|---------------|
| Small | 1-3 | $0.03-0.05 |
| Medium | 5-8 | $0.08-0.12 |
| Large | 13+ | $0.12-0.20 |

Break large stories (>13 points) into smaller units.

### 2. Batch Parallel Runs

Run multiple stories together to share cache:
- Stories 1-5 in single parallel-stories workflow
- Shared context cached across matrix jobs
- 50%+ additional savings from cache hits

### 3. Off-Peak Execution

Schedule workflows during off-peak hours for faster execution:
```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM UTC
```

### 4. Pre-Cache Context

Prime the cache before development runs:
```yaml
- name: Pre-cache Context
  env:
    CLAUDE_CODE_CACHE_ENABLED: true
  run: |
    claude -p "Read devforgeai/specs/context/*.md"
```

---

## Troubleshooting

### High Costs (>$0.20/story)

**Causes:** Haiku not enabled, caching disabled, complex story
**Solution:** Enable both caching and Haiku in github-actions.yaml

### Rate Limit Delays (429 errors)

**Cause:** Too many parallel jobs
**Solution:** Reduce max_parallel_jobs from 5 to 3

### Inconsistent Costs

**Causes:** Cache misses (>5min gaps), different models, retry loops
**Solution:** Enable caching, lock model version, add retry limits
