# Query Configuration Reference

**Loaded by:** Phase 02 (Query Routing & Subagent Orchestration)
**Purpose:** 6 query type configurations with descriptions, prompt templates, and parameter mapping

---

## Query Types Overview

| Query Type | Description | Prompt Focus | Required Params |
|------------|-------------|--------------|-----------------|
| dashboard | Generate dashboard metrics from session data | Extract workflow counts, error rates, completion times | none |
| workflows | Analyze workflow patterns from sessions | Group by workflow type, calculate success rates | none |
| errors | Extract error patterns from sessions | Find error messages, categorize by type, rank by frequency | none |
| decisions | Surface development decisions from sessions | Extract ADR references, AskUserQuestion interactions | optional: query_param |
| story | Deep analysis of specific story | Filter by story ID, extract timeline, identify key events | required: story_id |
| command-patterns | Extract high-frequency command sequences | Route to n-gram analysis, top 10 by frequency | none |

---

## Query Configuration Details

### Dashboard Query

**Purpose:** High-level overview of session activity and health metrics

**Prompt Template:**
```
Analyze Claude Code session history to generate a dashboard overview.
Focus: Extract total session counts, workflow execution frequency, error rates,
average completion times, and session duration distributions.
Return counts grouped by: workflow type, status (success/error/partial),
time period (daily/weekly).
```

**Aggregation Key:** `entry_type`
**Output Columns:** Metric, Value, Trend

---

### Workflows Query

**Purpose:** Analyze workflow patterns and execution frequencies

**Prompt Template:**
```
Analyze Claude Code session history to identify workflow patterns.
Focus: Group commands by workflow type (/dev, /qa, /create-story, /brainstorm, etc.),
calculate success rates per workflow, identify most frequent command sequences,
and track workflow completion times.
```

**Aggregation Key:** `content` (command/workflow name)
**Output Columns:** Workflow Type, Count, Success Rate

---

### Errors Query

**Purpose:** Identify common error patterns and failure points

**Prompt Template:**
```
Analyze Claude Code session history to extract error patterns.
Focus: Find all error messages, categorize by type (tool error, validation error,
timeout, permission denied, file not found), rank by frequency, identify recurring
failure patterns, and note the most recent occurrence of each error type.
```

**Aggregation Key:** `content` (error message)
**Output Columns:** Error Type, Count, Last Seen

---

### Decisions Query

**Purpose:** Surface architectural and implementation decisions made during development

**Prompt Template:**
```
Analyze Claude Code session history to surface development decisions.
Focus: Extract ADR references, AskUserQuestion interactions, technology choices,
architecture decisions, and implementation trade-offs discussed in sessions.
{IF query_param: Filter for decisions related to: "{query_param}"}
```

**Aggregation Key:** `metadata.story_id`
**Output Columns:** Date, Story, Decision, Rationale

---

### Story-Specific Query

**Purpose:** Deep analysis of a specific story's development history

**Prompt Template:**
```
Analyze Claude Code session history for story {story_id}.
Focus: Filter all entries related to {story_id}, extract the development timeline
(when each phase started/completed), identify key events (test failures, design decisions,
blockers), calculate phase durations, and summarize the story's development journey.
```

**Aggregation Key:** `metadata.phase`
**Output Columns:** Phase, Started, Completed, Duration

---

### Command-Patterns Query

**Purpose:** Identify high-frequency command sequences for workflow optimization

**Prompt Template:**
```
Analyze Claude Code session history to identify command sequence patterns.
Focus: Extract command n-grams (2-grams and 3-grams), rank by frequency,
calculate success rates for each sequence, identify the top 10 most common
command sequences. A command sequence is a series of commands executed in
consecutive order within a session.
```

**Aggregation Key:** `content` (command sequence)
**Output Columns:** Rank, Sequence, Frequency, Success Rate

---

## Common Parameters

All queries accept these optional parameters:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--days N` | Limit to last N days of data | null (all data) |
| `--force` | Force cache refresh | false |
| `--story-id STORY-XXX` | Required for story query | null |
| `"search string"` | Search filter for decisions query | null |

---

## Parameter-to-Prompt Mapping

When building the session-miner prompt, append these fragments based on parameters:

```
IF DAYS_LIMIT:
  append: f"Time window: Last {DAYS_LIMIT} days only."

IF STORY_ID:
  append: f"Filter: Only entries related to {STORY_ID}."

IF QUERY_PARAM:
  append: f"Search filter: '{QUERY_PARAM}'."

# Always append output format requirement:
append: "Return structured JSON with entries array containing SessionEntry objects."
append: "Each entry: timestamp, command, status (success|error|partial), duration_ms, user_input, model, session_id, project."
```
