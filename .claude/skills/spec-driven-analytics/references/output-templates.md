# Output Templates Reference

**Loaded by:** Phase 04 (Output Formatting & Caching)
**Purpose:** 6 query-specific markdown templates, table schemas, and formatting rules

---

## Common Template Structure

All templates follow a consistent 3-section structure:

```markdown
## {Query Title}

**Generated:** {timestamp} | **Period:** {period} | **Cache:** {hit|miss}

### Summary

{summary_metrics}

### {Results Section Name}

| {Column Headers} |
|{separators}|
| {data rows} |

### Recommendations

1. {recommendation_1}
2. {recommendation_2}
3. {recommendation_3}

---
*Source: session-miner subagent | Analytics ID: {ANALYTICS_ID} | Cached for: {ttl}s*
```

---

## Query-Specific Table Schemas

| Query Type | Results Section | Column Headers |
|------------|-----------------|----------------|
| dashboard | Key Metrics | Metric, Value, Trend |
| workflows | Workflow Distribution | Workflow Type, Count, Success Rate |
| errors | Top Errors by Frequency | Error Type, Count, Last Seen |
| decisions | Key Decisions | Date, Story, Decision, Rationale |
| story | Timeline | Phase, Started, Completed, Duration |
| command-patterns | Top Command Sequences | Rank, Sequence, Frequency, Success Rate |

---

## Template: Dashboard

```markdown
## Dashboard Overview

**Generated:** 2026-03-19T10:30:00Z | **Period:** All available data | **Cache:** miss

### Summary

**Total sessions analyzed:** 1,500
**Unique workflows:** 12
**Overall success rate:** 87.3%
**Average session duration:** 12.5 min

### Key Metrics

| Metric | Value | Trend |
|--------|-------|-------|
| Total Sessions | 1,500 | +15% vs last week |
| /dev Executions | 423 | Stable |
| /qa Executions | 312 | +8% |
| Error Rate | 12.7% | -3% (improving) |
| Avg Duration | 12.5 min | +2 min |

### Recommendations

1. Error rate has decreased 3% — current TDD practices are effective
2. /dev is the most-used workflow — consider performance optimization
3. Session duration trending up — may indicate increased complexity
```

---

## Template: Workflows

```markdown
## Workflow Distribution

**Generated:** {timestamp} | **Period:** {period} | **Cache:** {hit|miss}

### Summary

**Total workflow executions:** {count}
**Unique workflow types:** {categories}
**Highest success rate:** {top_workflow} ({rate}%)

### Workflow Patterns

| Workflow Type | Count | Success Rate |
|---------------|-------|-------------|
| /dev | 423 | 89.4% |
| /qa | 312 | 95.2% |
| /create-story | 187 | 97.3% |
| /brainstorm | 89 | 100.0% |

### Recommendations

1. /dev has lowest success rate — review common failure points
2. /qa success rate high — quality gates are effective
3. Consider automating common /create-story → /dev → /qa sequences
```

---

## Template: Errors

```markdown
## Error Analysis

**Generated:** {timestamp} | **Period:** {period} | **Cache:** {hit|miss}

### Summary

**Total errors found:** {count}
**Unique error types:** {categories}
**Most frequent:** {top_error}

### Top Errors by Frequency

| Error Type | Count | Last Seen |
|------------|-------|-----------|
| Sandbox permission denied | 45 | 2026-03-19 |
| Test assertion failure | 38 | 2026-03-18 |
| File not found | 22 | 2026-03-17 |
| Timeout exceeded | 15 | 2026-03-15 |

### Recommendations

1. Sandbox permission errors are most frequent — review sandbox config
2. Test assertion failures cluster around specific stories — investigate
3. File not found errors may indicate stale references in stories
```

---

## Template: Decisions

```markdown
## Decision Archive

**Generated:** {timestamp} | **Period:** {period} | **Cache:** {hit|miss}

### Summary

**Total decisions surfaced:** {count}
**Stories involved:** {categories}
**Search filter:** {query_param or "none"}

### Key Decisions

| Date | Story | Decision | Rationale |
|------|-------|----------|-----------|
| 2026-03-15 | STORY-460 | Use spec-driven pattern | Prevent token optimization bias |
| 2026-03-10 | STORY-445 | Adopt ADR-039 | Self-sufficient skill migration |
| 2026-03-05 | STORY-430 | Add W3 compliance | Prevent auto-skill chaining |

### Recommendations

1. Review ADR decisions for currency — some may need updates
2. Technology decisions should be validated against tech-stack.md
3. Architecture decisions cluster around skill migration — consider documenting patterns
```

---

## Template: Story Deep Dive

```markdown
## Story Deep Dive: {story_id}

**Generated:** {timestamp} | **Period:** All data for {story_id} | **Cache:** {hit|miss}

### Summary

**Story:** {story_id}
**Total events:** {count}
**Development duration:** {total_duration}
**Final status:** {status}

### Timeline

| Phase | Started | Completed | Duration |
|-------|---------|-----------|----------|
| Pre-Flight | 2026-03-19 10:00 | 2026-03-19 10:02 | 2 min |
| Red (Tests) | 2026-03-19 10:02 | 2026-03-19 10:15 | 13 min |
| Green (Impl) | 2026-03-19 10:15 | 2026-03-19 10:45 | 30 min |
| Refactor | 2026-03-19 10:45 | 2026-03-19 10:55 | 10 min |
| QA | 2026-03-19 11:00 | 2026-03-19 11:20 | 20 min |

### Recommendations

1. Green phase took longest — consider decomposing implementation
2. No blockers detected — clean development flow
3. QA passed first attempt — good test coverage in Red phase
```

---

## Template: Command Patterns

```markdown
## Command Sequence Analysis

**Generated:** {timestamp} | **Period:** {period} | **Cache:** {hit|miss}

### Summary

**Total sequences analyzed:** {count}
**Unique patterns:** {categories}
**Most common:** {top_pattern}

### Top Command Sequences

| Rank | Sequence | Frequency | Success Rate |
|------|----------|-----------|-------------|
| 1 | Read → Edit → Read | 156 | 94.2% |
| 2 | Glob → Read → Grep | 98 | 89.8% |
| 3 | Task → Read → Write | 67 | 85.1% |
| 4 | Read → Write → Glob | 45 | 97.8% |

### Recommendations

1. Read → Edit → Read is the dominant pattern — tool usage is following expected patterns
2. Task → Read → Write has lower success — investigate subagent integration issues
3. Consider bundling common sequences into reusable workflows
```

---

## No Results Template

When no data matches the query:

```markdown
## {Query Title}

**Generated:** {timestamp} | **Period:** {period} | **Cache:** miss

### No Results Found

No session data matched the query criteria.

**Troubleshooting:**
1. Verify session history exists at `~/.claude/history.jsonl`
2. Try broadening the time window (remove `--days` filter)
3. Check that the query type is correct: dashboard, workflows, errors, decisions, story, command-patterns
4. For story queries, verify the STORY-ID exists

**Try these alternative queries:**
- `/analytics` — Dashboard overview (default)
- `/analytics errors` — Error pattern analysis
- `/analytics workflows` — Workflow distribution
```

---

## Recommendation Generation

Recommendations are generated based on the data patterns:

1. **Identify outliers** — Metrics significantly above/below average
2. **Detect trends** — Increasing/decreasing patterns over time
3. **Surface correlations** — Related metrics that move together
4. **Suggest actions** — Concrete next steps based on findings

**Limit:** 3-5 recommendations per query. Quality over quantity.
