# Insights Command - Help & Reference

**Source:** Extracted from `/insights` command for lean orchestration compliance (STORY-461)

---

## Quick Reference

```bash
# Dashboard overview (default)
/insights

# Workflow pattern analysis
/insights workflows

# Error mining and analysis
/insights errors

# Decision archive search
/insights decisions [query]

# Story-specific insights
/insights story STORY-XXX

# Display help
/insights --help
```

---

## Help Section

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  /insights - Session Data Mining Query Interface
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DESCRIPTION:
  Execute insights queries to discover workflow patterns, errors,
  and decisions from DevForgeAI session data.

USAGE:
  /insights [query-type] [options]

QUERY TYPES:
  dashboard    Overview of session insights (default when no args)
  workflows    Analyze workflow patterns and command sequences
  errors       Mine error patterns and frequency analysis
  decisions    Search decision archive for architectural choices
  story        Get insights for a specific story
  command-patterns  Top 10 command sequences by frequency

PARAMETERS:
  [query]      Search string for 'decisions' query type
  STORY-XXX    Story ID for 'story' query type (e.g., STORY-224)

OPTIONS:
  --help, -h   Display this help message

EXAMPLES:
  /insights                         # Dashboard overview
  /insights workflows               # Workflow pattern analysis
  /insights errors                  # Error mining
  /insights decisions "caching"     # Search decisions about caching
  /insights story STORY-224         # Insights for STORY-224

INTEGRATION:
  Routes to devforgeai-insights skill which orchestrates:
  - session-miner subagent for data extraction
  - Pattern analysis algorithms
  - Report generation

RELATED COMMANDS:
  /feedback-search    Search feedback history
  /chat-search        Search chat history
  /rca                Root cause analysis

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Error Handling Details

### Invalid Query Type
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Error: Unknown query type
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Invalid query type: '[user-input]'

Valid query types:
  • dashboard         - Overview of session insights (default)
  • workflows         - Workflow pattern analysis
  • errors            - Error mining and frequency analysis
  • decisions         - Search decision archive
  • story             - Story-specific insights (requires STORY-ID)
  • command-patterns  - Top 10 command sequences by frequency

Usage: /insights [query-type] [options]
       /insights --help for more information
```

### Missing STORY-ID
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Error: Missing STORY-ID
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The 'story' query type requires a STORY-ID parameter.

Usage: /insights story STORY-XXX

Example: /insights story STORY-224

Run /insights --help for more information.
```

### Skill Not Found
```
Error: devforgeai-insights skill not available

Resolution:
1. Verify skill exists at .claude/skills/devforgeai-insights/SKILL.md
2. Run /create-context to ensure framework is configured
3. Check EPIC-034 implementation status
```

---

## Integration Notes

**Skill Dependency:**
- Requires `devforgeai-insights` skill (STORY-221)
- Skill orchestrates `session-miner` subagent (STORY-220)
- Session catalog from `STORY-223`

**Data Sources:**
- Session files in `.claude/sessions/`
- Feedback data in `devforgeai/feedback/`
- Story files in `devforgeai/specs/Stories/`

**Performance:**
- Command initialization < 2 seconds (NFR-CMD-001)
- Query execution time depends on data volume
