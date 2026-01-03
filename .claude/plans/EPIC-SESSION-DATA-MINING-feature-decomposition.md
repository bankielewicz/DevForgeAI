# Session Data Mining for Framework Intelligence - Feature Decomposition

**Status:** ANALYSIS COMPLETE
**Created:** 2025-01-02
**Purpose:** Transform Session Data Mining epic into detailed features with user stories and technical specifications
**Analyst:** Requirements Analyst (devforgeai-requirements-analyst skill)

---

## Executive Summary

The Session Data Mining epic will be decomposed into 5 major features, each delivering incremental business value. The total estimated effort spans 34 story points across the epic, with story sizes ranging from 2 to 8 points per feature.

**Key Findings:**
- Feature decomposition follows vertical slice pattern (each feature independently valuable)
- Stories properly sized for 1-2 sprint execution (2-5 points each)
- Technical dependencies form a linear progression (foundation → capabilities → integration)
- Data volume (86MB+) requires streaming/pagination for performance

---

## Feature Breakdown

### Feature 1: Session Miner Subagent - Data Extraction Foundation

**Feature Description:**
Foundation subagent that extracts, parses, and normalizes session data from multiple sources (history.jsonl, session files, plan files, todos). Provides data model layer for downstream analysis.

**Business Value:**
- Enables all subsequent insights capabilities
- Establishes single source of truth for session data
- Prepares framework for self-analysis and continuous improvement

**Story Point Estimate:** 8 points

**Architecture:**
- Component Type: Subagent (dedicated data layer)
- Tool Access: Read, Glob, Grep (data extraction)
- Output: Normalized data structures (JSON/objects)
- Performance Constraint: Handle 86MB+ data with streaming
- Framework Compliance: Single Responsibility (extraction only)

**Key User Stories:**

#### Story 1: Parse and Normalize history.jsonl Data
- **Points:** 3
- **User:** Framework Intelligence System
- **Goal:** Extract structured session metadata from history.jsonl
- **Acceptance Criteria:**
  - Parse JSON lines format with error tolerance
  - Extract: timestamp, command, status, duration, user inputs, model info
  - Handle malformed entries gracefully (log, skip, continue)
  - Support pagination for 86MB+ files (stream processing)
  - AC Verification: All records accessible, no data loss

#### Story 2: Extract Plan File Knowledge Base
- **Points:** 3
- **User:** Framework Intelligence System
- **Goal:** Mine decision context from .claude/plans/*.md files
- **Acceptance Criteria:**
  - Parse YAML frontmatter (status, created, author)
  - Extract story ID patterns with regex matching
  - Build decision archive (story → decision mapping)
  - Support cross-referencing via story IDs
  - AC Verification: 100% of story refs linked, frontmatter validated

#### Story 3: Catalog Session File Structure
- **Points:** 2
- **User:** Framework Intelligence System
- **Goal:** Inventory session artifacts and their relationships
- **Acceptance Criteria:**
  - Map .claude/plans/ → stories → artifacts
  - Build file dependency graph
  - Track session continuity markers
  - AC Verification: Graph complete, no orphaned files

**Dependencies:**
- None (foundation feature)

**Non-Functional Requirements:**
- **Performance:** Process 86MB+ data < 30 seconds (streaming)
- **Reliability:** 99% accuracy on data extraction (logged misses)
- **Scalability:** Horizontal scaling via parallel Glob patterns

**Technical Notes:**
- Use Glob with recursive patterns for massive file discovery
- Stream processing for history.jsonl (Bash loop + Read)
- Idempotent parsing (safe to re-run without side effects)

---

### Feature 2: DevForgeAI Insights Skill & /insights Command - Orchestration Layer

**Feature Description:**
Orchestration layer that coordinates session mining, presents user interface, and handles query routing. Central hub for all insights capabilities via /insights command.

**Business Value:**
- User-friendly interface to framework self-analysis
- On-demand intelligence without manual data gathering
- Integration point for all mining features

**Story Point Estimate:** 5 points

**Architecture:**
- Component Type: Skill + Slash Command
- Skill Invocation: `Skill(command="devforgeai-insights --query=patterns")`
- Command Invocation: `/insights --type=patterns --filter=errors`
- Tool Access: Task (invoke session-miner), Read (config), Write (results)
- Framework Compliance: Progressive disclosure pattern

**Key User Stories:**

#### Story 4: Create /insights Command with Query Routing
- **Points:** 3
- **User:** Developer
- **Goal:** Execute insights queries via command line interface
- **Acceptance Criteria:**
  - Support query parameters: --type, --filter, --output
  - Route to appropriate mining feature (patterns, errors, archive)
  - Provide usage help: `/insights --help`
  - AC Verification: All query types execute, errors reported clearly

#### Story 5: Implement devforgeai-insights Skill
- **Points:** 2
- **User:** Framework
- **Goal:** Orchestrate data mining and result presentation
- **Acceptance Criteria:**
  - Invoke session-miner subagent with query context
  - Format results for display (table, JSON, markdown)
  - Cache results (prevent re-mining within 1 hour)
  - AC Verification: Results formatted correctly, cache working

**Dependencies:**
- Feature 1: Session Miner Subagent (hard dependency)

**Non-Functional Requirements:**
- **Usability:** Command parameters match framework CLI standards
- **Performance:** Query execution < 10 seconds (cached)
- **Reliability:** Graceful error handling with user guidance

**Technical Notes:**
- Command keeps < 500 lines (size constraint)
- Progressive disclosure: main command → skill → subagent
- Configuration in devforgeai/config/insights.yaml

---

### Feature 3: Workflow Pattern Extraction - Command Sequence Analysis

**Feature Description:**
Mine command execution patterns from session history (frequency, sequences, success rates, branching). Analyze developer workflows to identify automation opportunities and best practices.

**Business Value:**
- Identify high-frequency command sequences for macros
- Quantify workflow success rates (measure framework effectiveness)
- Detect anti-patterns and improvement opportunities
- Drive continuous framework enhancement decisions

**Story Point Estimate:** 8 points

**Architecture:**
- Component Type: Subagent capability (extends session-miner)
- Query Type: `/insights --type=patterns`
- Output: Pattern frequency matrix, success rate heatmaps
- Algorithms: N-gram analysis, success/failure correlation

**Key User Stories:**

#### Story 6: Analyze Command Sequence Patterns
- **Points:** 3
- **User:** Framework Maintainer
- **Goal:** Identify high-frequency command sequences
- **Acceptance Criteria:**
  - Extract 2-gram, 3-gram command sequences
  - Calculate frequency and success rate per sequence
  - Identify top 10 sequences by frequency
  - Correlate sequences with story point estimates (pattern efficacy)
  - AC Verification: Sequences accurate, correlations validated

#### Story 7: Calculate Workflow Success Metrics
- **Points:** 3
- **User:** Framework Maintainer
- **Goal:** Quantify command and workflow success rates
- **Acceptance Criteria:**
  - Compute: completion rate, error rate, retry rate per command
  - Identify failure modes (most common errors)
  - Track recovery patterns (manual fixes, reruns)
  - Segment by story size (1 pt vs 5 pt vs 8 pt)
  - AC Verification: Metrics cover all commands, trends detected

#### Story 8: Identify Branching Points and Decision Trees
- **Points:** 2
- **User:** Framework Analyst
- **Goal:** Map conditional workflows (when developers choose different paths)
- **Acceptance Criteria:**
  - Detect commands that trigger multiple downstream choices
  - Build decision tree (command A → command B or C)
  - Measure branch probability (which path chosen %)
  - AC Verification: Trees complete, probabilities sum to 100%

**Dependencies:**
- Feature 1: Session Miner Subagent (hard)
- Feature 2: Insights Skill & Command (hard)

**Non-Functional Requirements:**
- **Performance:** Pattern analysis < 15 seconds for 86MB data
- **Accuracy:** N-gram analysis with 99% extraction accuracy
- **Insights:** Top 10 patterns should be actionable (not obvious)

**Technical Notes:**
- N-gram generation: sliding window over command sequence
- Success metrics: parse session status field (success/error/incomplete)
- Avoid spurious patterns: filter sequences < 5% frequency

---

### Feature 4: Anti-Pattern & Error Mining - Error Categorization and Recovery Tracking

**Feature Description:**
Deep error analysis from session history - categorize errors, track recovery patterns, identify recurring issues, and measure framework reliability.

**Business Value:**
- Identify top error categories for targeted fixes (RCA automation)
- Measure framework reliability and stability trends
- Track error recovery effectiveness (auto-fix success rates)
- Drive quality improvement roadmap

**Story Point Estimate:** 8 points

**Architecture:**
- Component Type: Subagent capability (extends session-miner)
- Query Type: `/insights --type=errors --severity=critical`
- Output: Error frequency heatmaps, recovery success rates
- Integration: Feed into RCA automation (EPIC-032)

**Key User Stories:**

#### Story 9: Categorize and Classify Session Errors
- **Points:** 3
- **User:** Framework Maintainer
- **Goal:** Organize errors by category and severity
- **Acceptance Criteria:**
  - Extract error messages from session logs
  - Classify: type (API, validation, timeout, etc.), severity (critical/high/medium/low)
  - Deduplicate: group equivalent errors (same root cause)
  - Assign error codes for tracking (ERR-001, ERR-002, etc.)
  - AC Verification: All errors categorized, dedup verified

#### Story 10: Track Error Recovery Patterns
- **Points:** 3
- **User:** Framework Analyst
- **Goal:** Analyze how developers recover from errors
- **Acceptance Criteria:**
  - Identify recovery actions post-error (retry, manual fix, skip)
  - Measure recovery success: did next attempt succeed?
  - Track retry count distribution (0-5 retries)
  - Identify which recovery actions work best per error type
  - AC Verification: Recovery chains complete, success rates calculated

#### Story 11: Mine Anti-Pattern Occurrences
- **Points:** 2
- **User:** Framework Analyst
- **Goal:** Detect usage of framework anti-patterns
- **Acceptance Criteria:**
  - Match commands against anti-patterns.md rules
  - Count violations by pattern type
  - Track consequences (did usage lead to errors?)
  - AC Verification: 100% pattern match, consequence link validated

**Dependencies:**
- Feature 1: Session Miner Subagent (hard)
- Feature 2: Insights Skill & Command (hard)

**Non-Functional Requirements:**
- **Performance:** Error analysis < 15 seconds
- **Accuracy:** Error classification 95%+ accurate
- **Insights:** Top 10 errors should represent 80%+ of issues

**Technical Notes:**
- Error classification: regex patterns + semantic keywords
- Recovery tracking: sequence correlation (error → next N commands)
- Deduplication: string similarity (levenshtein distance)

---

### Feature 5: Plan File Knowledge Base - Decision Archive Search and Context

**Feature Description:**
Build searchable decision archive from plan files - index decisions by story, date, and context. Enable developers to learn from previous architectural decisions and development approaches.

**Business Value:**
- Institutional knowledge preservation and searchability
- Reduce decision-making time (learn from history)
- Enable consistent architecture across projects
- Support RCA and retrospective analysis

**Story Point Estimate:** 5 points

**Architecture:**
- Component Type: Subagent capability (extends session-miner)
- Query Type: `/insights --type=archive --story=STORY-162 --search=pattern`
- Output: Indexed decision records, search results, context links
- Storage: In-memory index (regenerate on demand) or JSON cache

**Key User Stories:**

#### Story 12: Index Plan Files by Story and Decision Type
- **Points:** 2
- **User:** Framework
- **Goal:** Build searchable index of decisions from plan files
- **Acceptance Criteria:**
  - Parse frontmatter (story ID, status, created date)
  - Extract decision sections (## Decision, ## Technical Approach)
  - Index by: story ID, date, decision type, keywords
  - Support full-text search on decision content
  - AC Verification: Index complete, search queries work

#### Story 13: Search and Retrieve Decision Context
- **Points:** 2
- **User:** Developer
- **Goal:** Find architectural decisions and approaches for similar stories
- **Acceptance Criteria:**
  - Search by story ID: find all decisions for STORY-162
  - Search by date range: decisions in December 2025
  - Search by keywords: find pattern-related decisions
  - Retrieve full context: decision text, rationale, outcomes
  - AC Verification: All search queries return relevant results

#### Story 14: Link Decisions to Story Outcomes (Optional - Deferred)
- **Points:** 1 (deferred)
- **User:** Framework Analyst
- **Goal:** Correlate planning decisions with story outcomes
- **Acceptance Criteria:**
  - Link plan decisions to story status (delivered, deferred, failed)
  - Measure decision effectiveness (did approach work?)
  - Identify decision patterns that correlate with success
  - AC Verification: Links complete, correlation statistical significance > 0.7

**Dependencies:**
- Feature 1: Session Miner Subagent (hard)
- Feature 2: Insights Skill & Command (hard)
- Optional: STORY-163 (cross-reference framework - deferred)

**Non-Functional Requirements:**
- **Performance:** Index generation < 5 seconds, search < 1 second
- **Searchability:** Full-text search with partial matching
- **Scalability:** Support 1000+ plan files

**Technical Notes:**
- Index structure: JSON with nested story → decisions mapping
- Search: Grep patterns for keyword matching + Fuzzy string matching
- Cache index in .cache/insights-plan-index.json (gitignored)

---

## Feature Matrix Summary

| Feature | Points | Stories | Key Benefit | Dependencies |
|---------|--------|---------|-------------|--------------|
| 1. Session Miner | 8 | 3 | Foundation layer | None |
| 2. Insights Skill/Command | 5 | 2 | User interface | Feature 1 |
| 3. Workflow Patterns | 8 | 3 | Identify improvements | Features 1, 2 |
| 4. Error Mining | 8 | 3 | Quality improvement | Features 1, 2 |
| 5. Plan Archive | 5 | 3 | Knowledge preservation | Features 1, 2 |
| **TOTAL** | **34** | **14** | | |

---

## Story Validation Against INVEST Principles

### Independent (Vertical Slices)
- Feature 1 (Session Miner): Fully independent foundation
- Feature 2 (Skill/Command): Depends on Feature 1, but is independently valuable once Feature 1 complete
- Features 3-5: All depend on Features 1 & 2, but are otherwise independent of each other

**Mitigation:** Implement as sequential releases:
1. Sprint N: Feature 1
2. Sprint N+1: Feature 2 + optionally start Features 3-5 in parallel
3. Sprint N+2+: Features 3-5 in any order

### Negotiable
- Story acceptance criteria focus on "happy path" (success cases)
- Error handling details can be refined during implementation
- Performance targets (< 15 seconds) can be negotiated
- Example: "Exact N-gram algorithm negotiable, results must be actionable"

### Valuable
- Each story delivers measurable business value
- Session Miner: Enables self-analysis (framework learns from itself)
- Insights Command: Actionable intelligence for maintainers
- Patterns: Quantify workflow effectiveness (ROI on framework)
- Errors: Prioritize fixes by impact
- Archive: Preserve institutional knowledge

### Estimable
- Points assigned based on:
  - Complexity: JSON parsing (2-3), regex extraction (3), algorithm impl (3-5)
  - Volume: 86MB data requires optimization (adds 2-3 points)
  - Integration: Subagent creation, skill invocation (adds 1 point)
- Team can estimate similar data extraction tasks

### Small
- All stories fit within 1-2 sprint capacity (2-5 points each)
- Largest story (Story 6): 3 points = ~4-6 hours implementation
- No story exceeds 3 points except features that include entire feature complexity

### Testable
- Acceptance criteria specify testable outcomes
- Examples:
  - "All records accessible" = grep for record count, verify no data loss
  - "N-gram analysis with 99% accuracy" = unit test against known sequences
  - "Pattern analysis < 15 seconds" = timing benchmark
  - "Search queries return relevant results" = test with 5+ search patterns

---

## Technical Specifications Summary

### Data Models

**Session Record**
```
{
  timestamp: ISO8601,
  command: string,
  arguments: object,
  status: "success" | "error" | "partial",
  duration_ms: number,
  user_input: string[],
  model: string
}
```

**Error Record**
```
{
  error_code: string (ERR-001),
  message: string,
  category: string (api, validation, timeout, etc.),
  severity: "critical" | "high" | "medium" | "low",
  frequency: number,
  recovery_actions: string[],
  recovery_success_rate: float
}
```

**Decision Record**
```
{
  story_id: string,
  created_date: ISO8601,
  decision_type: string,
  content: string,
  keywords: string[],
  outcome: "delivered" | "deferred" | "failed" (optional)
}
```

### API Contracts (Skill Invocation)

**Query Pattern Results**
```
POST /insights/patterns
{
  top_sequences: [
    { sequence: ["cmd1", "cmd2"], frequency: 45, success_rate: 0.95 },
    ...
  ],
  workflow_branches: {
    "dev": { "qa": 0.85, "release": 0.15 },
    ...
  }
}
```

**Error Analysis Results**
```
POST /insights/errors
{
  error_categories: {
    "validation": { count: 234, severity: "high", recovery_rate: 0.78 },
    ...
  },
  top_errors: [
    { code: "ERR-001", message: "...", frequency: 45, recovery: "manual-fix" }
  ]
}
```

### Non-Functional Requirements

**Performance Targets:**
- Session Miner: Parse 86MB < 30 seconds
- Insights Command: Query execution < 10 seconds (cached)
- Pattern Analysis: < 15 seconds
- Error Analysis: < 15 seconds
- Archive Search: < 1 second

**Data Volume:**
- 86MB+ history.jsonl (streaming required)
- 100+ plan files
- 1000+ session records

**Reliability:**
- Error extraction: 95%+ accuracy
- Data loss: 0% (all valid records captured)
- Cache coherence: Regenerate on demand or hourly

**Security:**
- Plan files: No sensitive data extraction
- Error logs: Sanitize user inputs from error messages
- Archive: Public knowledge (no secrets)

---

## Implementation Sequencing & Dependencies

```
Timeline:
┌──────────────────────────────────────────────────┐
│ Sprint N: Feature 1 (Session Miner Subagent)     │
│ Stories 1-3: 8 points                             │
│ Deliverable: data extraction foundation          │
└──────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────┐
│ Sprint N+1: Feature 2 (Insights Skill/Command)   │
│ Stories 4-5: 5 points                             │
│ Deliverable: user interface to mining            │
└──────────────────────────────────────────────────┘
         │
         ├─────────────────┬──────────────────┬──────────┐
         ▼                 ▼                  ▼          ▼
    Feat 3: Patterns  Feat 4: Errors    Feat 5: Archive
    Stories 6-8       Stories 9-11       Stories 12-14
    8 points          8 points           5 points
    (parallel ok)     (parallel ok)      (parallel ok)
```

**Hard Dependencies:**
1. Feature 1 → Features 2, 3, 4, 5
2. Feature 2 → Features 3, 4, 5

**Soft Dependencies:**
- Feature 5 (Plan Archive) → STORY-163 (optional, defers link to outcomes)

---

## Risk Analysis

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| 86MB data causes timeouts | High | Medium | Implement streaming, pagination, early filtering |
| Error classification too broad/narrow | Medium | Medium | Test against sample 1000 errors, iterate categories |
| N-gram patterns too obvious | Low | Low | Filter by minimum frequency (5%) + filter obviousness |
| Plan file structure varies too much | Medium | Low | Use flexible regex + frontmatter validation |
| Cache invalidation complexity | Medium | Medium | Regenerate on-demand (simple but slower) vs incremental (complex) |

---

## Success Criteria for Epic

- [ ] All 14 stories implemented and passing tests
- [ ] Session Miner correctly extracts 100% of session data
- [ ] /insights command functional for all 5 query types
- [ ] Pattern analysis identifies top 10 sequences (actionable)
- [ ] Error mining covers all error types (0 missing categories)
- [ ] Plan archive searchable by story, date, keyword
- [ ] Performance targets met (< 15 sec per query)
- [ ] Zero data loss during mining (100% record capture)
- [ ] Framework demonstrates self-analysis capability

---

## Reference Links

**Framework Standards:**
- Tech Stack: `/devforgeai/specs/context/tech-stack.md`
- Architecture Constraints: `/devforgeai/specs/context/architecture-constraints.md`
- Coding Standards: `/devforgeai/specs/context/coding-standards.md`

**Related Epics:**
- EPIC-032: RCA to Story Automation (consumes error mining output)
- EPIC-021: Expertise System Foundation (builds on decision archive)
- EPIC-023: Self-Improvement Automation (uses pattern insights)

**Example Stories:**
- See `/devforgeai/specs/Stories/` for story template format

---

## Next Steps

1. **User Validation:** Confirm feature breakdown aligns with business goals
2. **Story Creation:** Generate detailed story files using requirements-analyst skill
3. **Technical Design:** Create ADRs for data model and algorithm choices
4. **Sprint Planning:** Sequence features across sprints (recommend 3-4 sprints total)
5. **Implementation:** Execute Feature 1 (Session Miner) as foundation
