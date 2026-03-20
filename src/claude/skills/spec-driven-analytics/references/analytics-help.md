# Analytics Command - Help & Reference

**Source:** Migrated from `/insights` command help (STORY-461), updated for `/analytics` command
**Loaded by:** Phase 00 (when --help flag provided)

---

## Quick Reference

```bash
# Dashboard overview (default)
/analytics

# Workflow pattern analysis
/analytics workflows

# Error mining and analysis
/analytics errors

# Decision archive search
/analytics decisions [query]

# Story-specific analytics
/analytics story STORY-XXX

# Command sequence analysis
/analytics command-patterns

# Force cache refresh
/analytics --force workflows

# Limit to last 7 days
/analytics --days 7 errors

# Display help
/analytics --help
```

---

## Help Section

```
------------------------------------------------------------
  /analytics - Session Data Mining & Analytics Interface
------------------------------------------------------------

DESCRIPTION:
  Execute analytics queries to discover workflow patterns, errors,
  and decisions from DevForgeAI session data. Uses spec-driven
  workflow with structural anti-skip enforcement.

USAGE:
  /analytics [query-type] [options]

QUERY TYPES:
  dashboard         Overview of session analytics (default when no args)
  workflows         Analyze workflow patterns and command sequences
  errors            Mine error patterns and frequency analysis
  decisions         Search decision archive for architectural choices
  story             Get analytics for a specific story
  command-patterns  Top 10 command sequences by frequency

PARAMETERS:
  [query]           Search string for 'decisions' query type
  STORY-XXX         Story ID for 'story' query type (e.g., STORY-224)

OPTIONS:
  --force           Force cache refresh (bypass 1-hour TTL)
  --days N          Limit to last N days of data
  --help, -h        Display this help message

EXAMPLES:
  /analytics                              # Dashboard overview
  /analytics workflows                    # Workflow pattern analysis
  /analytics errors                       # Error mining
  /analytics decisions "caching"          # Search decisions about caching
  /analytics story STORY-224              # Analytics for STORY-224
  /analytics command-patterns             # Command sequence analysis
  /analytics --force errors               # Fresh error analysis
  /analytics --days 7 workflows           # Last 7 days of workflows

INTEGRATION:
  Routes to spec-driven-analytics skill which orchestrates:
  - session-miner subagent for data extraction
  - Pattern analysis and aggregation pipeline
  - Cached report generation (1-hour TTL)

RELATED COMMANDS:
  /feedback-search    Search feedback history
  /chat-search        Search chat history
  /rca                Root cause analysis

------------------------------------------------------------
```

---

## Error Handling Details

### Invalid Query Type
```
------------------------------------------------------------
  Error: Unknown query type
------------------------------------------------------------

Invalid query type: '[user-input]'

Valid query types:
  - dashboard         - Overview of session analytics (default)
  - workflows         - Workflow pattern analysis
  - errors            - Error mining and frequency analysis
  - decisions         - Search decision archive
  - story             - Story-specific analytics (requires STORY-ID)
  - command-patterns  - Top 10 command sequences by frequency

Usage: /analytics [query-type] [options]
       /analytics --help for more information
```

### Missing STORY-ID
```
------------------------------------------------------------
  Error: Missing STORY-ID
------------------------------------------------------------

The 'story' query type requires a STORY-ID parameter.

Usage: /analytics story STORY-XXX

Example: /analytics story STORY-224

Run /analytics --help for more information.
```

### Skill Not Found
```
Error: spec-driven-analytics skill not available

Resolution:
1. Verify skill exists at src/claude/skills/spec-driven-analytics/SKILL.md
2. Run /create-context to ensure framework is configured
3. Check skill registration in system prompt
```

---

## Integration Notes

**Skill Dependency:**
- Requires `spec-driven-analytics` skill
- Skill orchestrates `session-miner` subagent
- Results cached in `devforgeai/cache/analytics/`

**Data Sources:**
- Session files in `~/.claude/history.jsonl`
- Feedback data in `devforgeai/feedback/`
- Story files in `devforgeai/specs/Stories/`

**Performance:**
- Cache hit: <2 seconds (read from disk)
- Cache miss: 10-60 seconds (depends on data volume)
- Force refresh: Same as cache miss
