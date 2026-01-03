# Session Data Mining - Features Breakdown

**Status:** DOCUMENTED
**Last Updated:** 2025-01-02
**Version:** 1.0

---

## Quick Reference Matrix

| # | Feature | Points | Stories | Key Deliverable | Dependencies |
|---|---------|--------|---------|-----------------|--------------|
| 1 | Session Miner Subagent | 8 | 3 | Data extraction layer | None |
| 2 | Insights Skill & Command | 5 | 2 | User interface (/insights) | #1 |
| 3 | Workflow Patterns | 8 | 3 | Pattern mining & metrics | #1, #2 |
| 4 | Error Mining | 8 | 3 | Error categorization | #1, #2 |
| 5 | Plan Archive | 5 | 3 | Decision knowledge base | #1, #2 |

---

## Feature 1: Session Miner Subagent

### Overview
Foundation data extraction subagent that parses history.jsonl, session files, plan files, and todos into normalized data structures. Provides single source of truth for all downstream analysis.

### Business Value
- Enables framework self-analysis capability
- Establishes data foundation for all insights features
- Supports framework continuous improvement

### Scope
**In Scope:**
- Parse history.jsonl (86MB+, streaming required)
- Extract plan file metadata and structure
- Catalog session artifacts
- Normalize data formats
- Handle errors gracefully

**Out of Scope:**
- Analysis or interpretation of data
- Caching (pass-through only)
- Real-time monitoring

### Stories (8 points total)

#### STORY-???: Parse history.jsonl with Streaming
- **Points:** 3
- **User Story:** As a framework intelligence system, I want to parse history.jsonl with streaming to extract session metadata without loading entire 86MB file into memory.
- **Key Acceptance Criteria:**
  - Parse JSON lines format (one JSON object per line)
  - Extract fields: timestamp, command, arguments, status, duration_ms, user_input, model
  - Pagination support for large datasets
  - Error tolerance: malformed lines logged and skipped
  - Performance: Process 86MB < 30 seconds
- **Technical Notes:**
  - Implementation: Bash loop with `Read` tool (streaming pattern)
  - Error handling: Logged skipped lines, count reported
  - Output format: Newline-delimited JSON (preserves streaming)

#### STORY-???: Extract Plan File Knowledge Base
- **Points:** 3
- **User Story:** As a framework intelligence system, I want to extract decision context from plan files to build decision archive.
- **Key Acceptance Criteria:**
  - Parse YAML frontmatter (status, created, author, story)
  - Extract decision sections via regex (## Decision, ## Technical Approach)
  - Build mapping: story_id → plan_file → decisions
  - Support cross-reference by story ID
  - Handle 100+ plan files without timeout
- **Technical Notes:**
  - Frontmatter parsing: Regex pattern for YAML block
  - Story ID extraction: Pattern `STORY-\d+` with word boundaries
  - Index structure: JSON with nested objects

#### STORY-???: Catalog Session File Structure
- **Points:** 2
- **User Story:** As a framework intelligence system, I want to catalog session files and build artifact dependency graph.
- **Key Acceptance Criteria:**
  - Map file relationships: plan → stories → artifacts
  - Track session continuity (session A → session B markers)
  - Inventory all session artifacts with timestamps
  - Build dependency graph (no orphaned files)
  - Validation: 100% coverage, no missing nodes
- **Technical Notes:**
  - Glob patterns: Recursive discovery of .claude/plans/
  - Graph structure: Adjacency list in JSON
  - Continuity detection: Regex for plan file naming patterns

### Technical Specifications

**Component Type:** Subagent (`.claude/agents/session-miner.md`)

**Tool Access:**
- Read - Parse files
- Glob - Discover files
- Grep - Extract patterns

**Input Parameters:**
```yaml
mining_type: "all" | "history" | "plans" | "sessions"
output_format: "json" | "jsonl"
pagination: { limit: 1000, offset: 0 }
```

**Output Data Structure:**
```json
{
  "sessions": [
    {
      "timestamp": "2025-01-01T12:00:00Z",
      "command": "dev",
      "status": "success",
      "duration_ms": 45000
    }
  ],
  "decisions": [
    {
      "story_id": "STORY-162",
      "plan_file": "STORY-162-plan-name.md",
      "content": "Decision text"
    }
  ],
  "artifacts": [
    {
      "file": ".claude/plans/file.md",
      "type": "plan",
      "references": ["STORY-001", "STORY-002"]
    }
  ]
}
```

**Performance Requirements:**
- Input: 86MB+ data
- Latency: < 30 seconds for full parse
- Memory: Streaming (no full file load)
- Error Rate: < 1% (malformed lines acceptable)

**Non-Functional Requirements:**
- Idempotent (safe to re-run)
- Fault-tolerant (continue on errors)
- Extensible (new data sources via config)

---

## Feature 2: Insights Skill & /insights Command

### Overview
Orchestration layer providing user interface to session mining via `/insights` command and `devforgeai-insights` skill. Routes queries to appropriate mining features and formats results.

### Business Value
- Accessible interface for framework self-analysis
- On-demand intelligence without manual data gathering
- Central hub for all insights capabilities

### Scope
**In Scope:**
- /insights command implementation
- Query routing (patterns, errors, archive)
- Result formatting (table, JSON, markdown)
- Caching (avoid re-mining within 1 hour)
- Error handling with user guidance

**Out of Scope:**
- Data mining (delegated to Feature 1)
- Analysis algorithms (delegated to Features 3-5)
- Persistent storage (cache only)

### Stories (5 points total)

#### STORY-???: Implement /insights Command
- **Points:** 3
- **User Story:** As a developer, I want to execute insights queries via `/insights` command to analyze framework behavior.
- **Key Acceptance Criteria:**
  - Support query types: patterns, errors, archive
  - Support filters: --story, --type, --date-range, --severity
  - Support output: --output=json|table|markdown
  - Provide usage help: `/insights --help`
  - Error handling: Clear error messages with resolution
  - Max execution time: 10 seconds
- **Technical Notes:**
  - Command location: `.claude/commands/insights.md`
  - Size constraint: < 500 lines (~ 20K chars)
  - Parameter parsing: Use $ARGUMENTS placeholder
  - Progressive disclosure: Main command → skill → subagent

#### STORY-???: Implement devforgeai-insights Skill
- **Points:** 2
- **User Story:** As the framework, I want a skill to orchestrate mining and format results.
- **Key Acceptance Criteria:**
  - Invoke session-miner subagent with query parameters
  - Format results for display (table, JSON, markdown)
  - Implement caching: results valid 1 hour
  - Support batch queries (multiple insights in one skill invocation)
  - Performance: < 5 seconds (with cache)
- **Technical Notes:**
  - Skill location: `.claude/skills/devforgeai-insights/SKILL.md`
  - Size target: 500-800 lines
  - Cache storage: `.cache/insights-results.json` (gitignored)
  - Cache key: hash(query parameters)

### Technical Specifications

**Slash Command:** `/insights`

**Usage Examples:**
```bash
# Show top 10 workflow patterns
/insights --type=patterns --limit=10

# Show errors for past week
/insights --type=errors --severity=high --date-range=7d

# Search decisions by story
/insights --type=archive --story=STORY-162

# Get error recovery strategies
/insights --type=errors --filter=recovery_success_rate
```

**Skill Invocation:**
```
Skill(command="devforgeai-insights --type=patterns --output=json")
```

**Output Formats:**

Table (default):
```
Workflow Pattern        | Frequency | Success Rate
-----------------------+-----------+-------------
dev → qa → release      | 45        | 95%
dev → qa → defer        | 12        | 78%
```

JSON:
```json
{
  "patterns": [
    {
      "sequence": ["dev", "qa", "release"],
      "frequency": 45,
      "success_rate": 0.95
    }
  ]
}
```

**Configuration File:** `devforgeai/config/insights.yaml`
```yaml
mining:
  cache_ttl_seconds: 3600
  session_miner_timeout: 30
  query_timeout: 10

output:
  default_format: table
  max_results: 20

sources:
  history_jsonl: ~/.claude/history.jsonl
  plans_dir: .claude/plans/
```

---

## Feature 3: Workflow Pattern Extraction

### Overview
Mine command execution patterns (2-grams, 3-grams), analyze success rates, identify branching points, and measure workflow effectiveness. Provides metrics for framework optimization.

### Business Value
- Identify high-frequency patterns for automation
- Quantify workflow effectiveness (measure framework ROI)
- Detect anti-patterns and improvement opportunities
- Drive framework enhancement roadmap

### Scope
**In Scope:**
- N-gram analysis (2-gram, 3-gram command sequences)
- Success rate calculation per pattern
- Branching point detection
- Correlation with story point estimates
- Top-10 patterns reporting

**Out of Scope:**
- Prediction (this feature reports history, not future)
- Optimization recommendations (framework maintainer decides)
- Long-term trend analysis (scope to single quarter)

### Stories (8 points total)

#### STORY-???: Analyze Command Sequence Patterns
- **Points:** 3
- **User Story:** As a framework maintainer, I want to analyze command sequence patterns to identify high-frequency workflows.
- **Key Acceptance Criteria:**
  - Extract 2-gram and 3-gram command sequences
  - Count frequency of each sequence
  - Calculate success rate (% sequences ending in success)
  - Report top 10 by frequency
  - Handle missing or incomplete sequences gracefully
- **Technical Notes:**
  - Algorithm: Sliding window over command sequence
  - Sequence key: tuple of commands (deterministic)
  - Success detection: Last command status in sequence
  - Minimum frequency filter: >= 5% to avoid noise

#### STORY-???: Calculate Workflow Success Metrics
- **Points:** 3
- **User Story:** As a framework maintainer, I want to calculate success metrics per command to identify reliability issues.
- **Key Acceptance Criteria:**
  - Compute per-command: completion_rate, error_rate, retry_count
  - Identify top 5 error modes (most frequent errors per command)
  - Track recovery patterns (manual fixes, reruns, skips)
  - Segment metrics by story size (1pt vs 5pt vs 8pt)
  - Report trends over time (weekly success rate changes)
- **Technical Notes:**
  - Completion: (successful runs) / (total runs)
  - Error rate: (errored runs) / (total runs)
  - Recovery: track commands immediately after errors
  - Segmentation: extract story size from context

#### STORY-???: Identify Branching Points and Decision Trees
- **Points:** 2
- **User Story:** As a framework analyst, I want to identify workflow branching points to understand decision patterns.
- **Key Acceptance Criteria:**
  - Detect commands with multiple downstream choices
  - Build decision tree (command → [next_commands])
  - Calculate branch probability (% choosing each branch)
  - Identify correlations (does story size affect branch choice?)
  - Validate: branch probabilities sum to 100%
- **Technical Notes:**
  - Branching: command_n → N possible command_n+1 choices
  - Probability: (count of branch) / (total occurrences of command)
  - Correlation: cross-tabulation with story size

### Technical Specifications

**Query Type:** `/insights --type=patterns`

**Output Structure:**
```json
{
  "top_sequences": [
    {
      "sequence": ["dev", "qa", "release"],
      "frequency": 45,
      "success_rate": 0.95,
      "avg_story_points": 3.2
    }
  ],
  "command_metrics": {
    "dev": {
      "completion_rate": 0.92,
      "error_rate": 0.08,
      "avg_retry_count": 1.3,
      "top_errors": ["ERR-001", "ERR-005"]
    }
  },
  "branching_points": {
    "dev": {
      "qa": { "count": 45, "probability": 0.85 },
      "release": { "count": 8, "probability": 0.15 }
    }
  }
}
```

**Algorithm Complexity:**
- N-gram generation: O(N) where N = total commands
- Frequency calculation: O(N * K) where K = avg sequence length
- Overall: O(N) for linear scan

**Performance Target:**
- Parse 1000+ session records: < 15 seconds
- Memory: O(K) where K = unique sequences (typically < 100)

---

## Feature 4: Anti-Pattern & Error Mining

### Overview
Deep error analysis from session history - categorize errors, track recovery patterns, measure framework reliability. Identifies top error types and effective recovery strategies.

### Business Value
- Identify top error categories for targeted fixes
- Measure framework stability and reliability trends
- Track error recovery effectiveness
- Drive quality improvement roadmap
- Feed into RCA automation (EPIC-032)

### Scope
**In Scope:**
- Error extraction from session logs
- Error classification (type, severity, category)
- Deduplication (group equivalent errors)
- Recovery tracking (what actions recover from error)
- Recovery success measurement

**Out of Scope:**
- Root cause analysis (separate - EPIC-032)
- Automated fixes (future enhancement)
- Cross-framework error patterns

### Stories (8 points total)

#### STORY-???: Categorize and Classify Session Errors
- **Points:** 3
- **User Story:** As a framework maintainer, I want to categorize errors to understand failure modes.
- **Key Acceptance Criteria:**
  - Extract error messages from session logs
  - Classify by type (api, validation, timeout, permission, etc.)
  - Classify by severity (critical, high, medium, low)
  - Deduplicate equivalent errors (group by root cause)
  - Assign error codes (ERR-001, ERR-002, etc.)
  - Report: top 10 errors by frequency
- **Technical Notes:**
  - Type classification: Regex + semantic keywords
  - Severity: Based on impact (crash vs warning)
  - Deduplication: String similarity (levenshtein distance > 0.8)
  - Error code: Hash of normalized error message

#### STORY-???: Track Error Recovery Patterns
- **Points:** 3
- **User Story:** As a framework analyst, I want to track recovery patterns to identify effective error handling strategies.
- **Key Acceptance Criteria:**
  - Identify recovery actions post-error (retry, manual fix, skip, abort)
  - Measure recovery success: did next attempt succeed?
  - Calculate recovery success rate per error type
  - Track retry distribution (0-5+ retries)
  - Identify which recovery actions work best
- **Technical Notes:**
  - Recovery action: Command immediately following error
  - Success: Next command in sequence completed successfully
  - Retry: Same command executed again
  - Manual fix: Different command than error source

#### STORY-???: Mine Anti-Pattern Occurrences
- **Points:** 2
- **User Story:** As a framework analyst, I want to detect usage of anti-patterns to measure compliance.
- **Key Acceptance Criteria:**
  - Match session commands against anti-patterns.md rules
  - Count violations by pattern type
  - Track consequences: did violation lead to errors?
  - Identify users with highest violation count (anonymized)
  - Report: correlation between violations and errors
- **Technical Notes:**
  - Pattern matching: Load anti-patterns.md, match commands
  - Consequence tracking: Did error follow within N commands?
  - Correlation: Statistical measure (chi-square test)

### Technical Specifications

**Query Type:** `/insights --type=errors --severity=high`

**Output Structure:**
```json
{
  "error_categories": {
    "validation": {
      "count": 234,
      "severity": "high",
      "recovery_rate": 0.78,
      "top_recovery": "retry"
    },
    "timeout": {
      "count": 45,
      "severity": "medium",
      "recovery_rate": 0.65,
      "top_recovery": "manual_fix"
    }
  },
  "top_errors": [
    {
      "code": "ERR-001",
      "message": "Field required: story_id",
      "frequency": 45,
      "severity": "high",
      "recovery_actions": ["retry: 0.80", "manual_fix: 0.15", "abort: 0.05"],
      "affected_stories": ["STORY-162", "STORY-163"]
    }
  ],
  "anti_pattern_violations": {
    "bash_for_files": {
      "count": 12,
      "error_correlation": 0.75,
      "consequence_examples": ["ERR-003", "ERR-007"]
    }
  }
}
```

**Error Severity Levels:**
- **CRITICAL:** System crash, data loss, security breach (immediate action required)
- **HIGH:** Workflow blocked, feature unavailable, data inconsistency (fix in next sprint)
- **MEDIUM:** Degraded performance, partial functionality (fix when convenient)
- **LOW:** Documentation issue, cosmetic problem (backlog)

**Performance Target:**
- Analyze 1000+ errors: < 15 seconds
- Recovery tracking: < 5 seconds
- Anti-pattern matching: < 10 seconds

---

## Feature 5: Plan File Knowledge Base

### Overview
Build searchable decision archive from plan files. Index decisions by story, date, and keywords. Enable developers to learn from previous architectural decisions and approaches.

### Business Value
- Institutional knowledge preservation
- Reduced decision-making time (learn from history)
- Consistent architecture across projects
- Support RCA retrospective analysis
- Feed into expertise system (EPIC-021)

### Scope
**In Scope:**
- Index plan files by story ID, date, decision type
- Full-text search on decision content
- Retrieve decision context and rationale
- Link decisions to story outcomes (optional)
- Support 100+ plan files

**Out of Scope:**
- Decision effectiveness automation (future)
- Machine learning recommendations (future)
- Cross-project knowledge base (scope to DevForgeAI)

### Stories (5 points total)

#### STORY-???: Index Plan Files by Story and Decision Type
- **Points:** 2
- **User Story:** As the framework, I want to index plan files to enable decision search.
- **Key Acceptance Criteria:**
  - Parse plan file frontmatter (story_id, status, created, author)
  - Extract decision sections (## Decision, ## Technical Approach)
  - Build index: story_id → decisions mapping
  - Support full-text search on content
  - Index generation: < 5 seconds for 100 files
- **Technical Notes:**
  - Index structure: JSON with nested objects
  - Cache location: `.cache/insights-plan-index.json`
  - Update trigger: On-demand (regenerate each query) or hourly
  - Indexing: Grep for headers, Read for content

#### STORY-???: Search and Retrieve Decision Context
- **Points:** 2
- **User Story:** As a developer, I want to search decisions to learn from similar problems.
- **Key Acceptance Criteria:**
  - Search by story ID: retrieve all decisions for STORY-162
  - Search by date range: decisions in December 2025
  - Search by keywords: pattern-related decisions
  - Search by decision type: architecture, implementation, testing
  - Retrieve full context: text, rationale, outcomes
  - Performance: < 1 second per search query
- **Technical Notes:**
  - Search implementation: Grep patterns + fuzzy matching
  - Keyword extraction: Regex on decision section
  - Result ranking: Relevance score (keyword matches + recency)

#### STORY-???: Link Decisions to Story Outcomes (Optional - Deferred)
- **Points:** 1 (deferred)
- **User Story:** As a framework analyst, I want to correlate decisions with outcomes to measure decision quality.
- **Key Acceptance Criteria:**
  - Link plan decisions to story status (delivered, deferred, failed)
  - Calculate decision effectiveness (success rate per decision type)
  - Identify patterns in successful decisions
  - AC Verification: Correlation coefficient > 0.7 for patterns
- **Dependencies:** STORY-163 (cross-reference framework)
- **Deferral Justification:** Non-critical for MVP, requires outcome tracking

### Technical Specifications

**Query Type:** `/insights --type=archive --story=STORY-162`

**Output Structure:**
```json
{
  "decisions": [
    {
      "story_id": "STORY-162",
      "plan_file": "STORY-162-rca-011-cross-reference-update.md",
      "created": "2025-12-09T10:30:00Z",
      "decision_type": "architecture",
      "keywords": ["cross-reference", "rca", "framework"],
      "content": "Decision text excerpt...",
      "outcome": "delivered"
    }
  ],
  "total_decisions": 5,
  "search_quality": 0.92
}
```

**Index Structure:**
```json
{
  "by_story": {
    "STORY-162": [
      {
        "plan_file": "...",
        "decision_type": "...",
        "created": "..."
      }
    ]
  },
  "by_date": {
    "2025-12": [
      {
        "story_id": "...",
        "plan_file": "..."
      }
    ]
  },
  "by_keyword": {
    "architecture": [
      {
        "story_id": "...",
        "plan_file": "..."
      }
    ]
  }
}
```

**Search Performance:**
- Index generation: < 5 seconds (100 files)
- Search execution: < 1 second (cached index)
- Memory: O(F) where F = total files (< 5MB for 100 files)

---

## Implementation Roadmap

### Phase 1: Foundation (Sprint N)
**Feature:** Session Miner Subagent
**Stories:** 1-3 (8 points)
**Deliverable:** Data extraction layer
**Dependencies:** None
**Success Criteria:** 100% data extraction, < 30 second parse time

### Phase 2: Interface (Sprint N+1)
**Features:** Insights Skill & Command
**Stories:** 4-5 (5 points)
**Deliverable:** /insights command accessible
**Dependencies:** Feature 1
**Success Criteria:** All query types work, < 10 second execution

### Phase 3: Capabilities (Sprint N+2, N+3, N+4 - Parallel)
**Features:** Patterns, Errors, Archive
**Stories:** 6-14 (21 points)
**Deliverable:** Full mining capabilities
**Dependencies:** Features 1 & 2
**Parallelization:** Execute Features 3-5 in parallel (independent)
**Success Criteria:** All queries returning insights, performance targets met

---

## Success Metrics

| Metric | Target | Validation |
|--------|--------|-----------|
| Data Extraction Completeness | 100% | Verify all records extracted |
| Parse Performance | < 30 sec | Benchmark 86MB dataset |
| Query Performance | < 10 sec | Time /insights command |
| Pattern Actionability | 8/10 | Maintainer review |
| Error Coverage | 95%+ | Categorize sample 1000 errors |
| Archive Searchability | 99% | Test 50+ search queries |
| Framework Self-Analysis Enabled | Yes | Demonstrate /insights usage |

---

## Risk Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| 86MB file causes OOM | High | Medium | Implement true streaming (Bash + Read) |
| Error classification too broad | Medium | Medium | Validate against 1000 error samples |
| N-gram patterns obvious | Low | Low | Filter by minimum frequency |
| Plan files format variance | Medium | Low | Use flexible regex + fallback |
| Cache invalidation timing | Medium | Medium | Simple: regenerate on-demand |

---

## References

**Context Files:**
- Tech Stack: `devforgeai/specs/context/tech-stack.md`
- Architecture Constraints: `devforgeai/specs/context/architecture-constraints.md`

**Related Components:**
- Session Recovery: EPIC-024
- Expertise System: EPIC-021
- Self-Improvement: EPIC-023
- RCA Automation: EPIC-032

**Framework Status:**
- Framework Version: 1.0.1
- Production Ready: Yes
- Skills Available: 15 functional
- Subagents Available: 26

