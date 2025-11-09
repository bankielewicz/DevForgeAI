---
id: STORY-016
title: Searchable Metadata Index for Feedback Sessions
epic: EPIC-004
sprint: Sprint-2
status: Backlog
points: 13
priority: Medium
tags:
  - feedback-system
  - search
  - performance
  - indexing
  - storage
created: 2025-11-07
last-updated: 2025-11-07
---

# STORY-016: Searchable Metadata Index for Feedback Sessions

**Status**: Backlog
**Priority**: High
**Story Points**: 13
**Epic**: EPIC-002 (Feedback Capture and Interaction)
**Sprint**: [To be assigned during sprint planning]

## User Story

As a developer troubleshooting issues,
I want to search feedback sessions by date, operation, status, tags, and keywords,
So that I can quickly identify patterns (e.g., "all failed /qa runs in the last month") and priorities (e.g., "feedback mentioning confusing error messages") without manually reviewing hundreds of session files.

---

## Acceptance Criteria

### Scenario 1: Create and Update Index Entry on Feedback Write (Happy Path)
- **Given** a feedback session is written to `.devforgeai/feedback/sessions/[timestamp]-[operation]-[status].md`
- **When** the feedback session file is created successfully
- **Then** a new entry is automatically appended to `.devforgeai/feedback/index.json` with:
  - Unique `id` field (format: `[timestamp]-[operation]-[status]`, matching filename)
  - `timestamp` in ISO 8601 format (e.g., `2025-11-07T10:30:00Z`)
  - `operation.type` (e.g., "command", "skill", "subagent")
  - `operation.name` (e.g., "/dev", "devforgeai-qa", "test-automator")
  - `operation.args` (e.g., "STORY-042", "deep mode")
  - `status` field ("success", "failure", "partial")
  - `tags` array (extracted from session content)
  - `story-id` if applicable (extracted from operation.args or session content)
  - `keywords` array (extracted from session content, 3-5 relevant terms)
  - `file-path` (relative path to session file)
  - Index file is valid JSON and maintains proper formatting

### Scenario 2: Index File Format Validation (Happy Path)
- **Given** the index file `.devforgeai/feedback/index.json` is created
- **When** the file is read
- **Then** it contains:
  - `version` field = "1.0"
  - `last-updated` field in ISO 8601 format (updated on each index write)
  - `feedback-sessions` array with zero or more entry objects
  - All required fields present in each entry (id, timestamp, operation, status, tags, story-id, keywords, file-path)
  - All timestamps are valid ISO 8601 format
  - All tags are lowercase strings
  - Keywords are lowercase and hyphenated if multi-word
  - No duplicate `id` values in the array

### Scenario 3: Search by Date Range (Happy Path)
- **Given** index contains 50 feedback sessions from the last 90 days
- **When** user searches with filters: `date-start: 2025-10-07, date-end: 2025-11-07`
- **Then** results include only sessions where `timestamp` falls within the range (inclusive)
- **And** results are returned in reverse chronological order (newest first)
- **And** search completes in under 500ms

### Scenario 4: Search by Operation Type and Name (Happy Path)
- **Given** index contains sessions from multiple operations (/dev, /qa, /create-story, devforgeai-development, etc.)
- **When** user searches with filters: `operation-type: "command", operation-name: "/qa"`
- **Then** results include only sessions where `operation.type == "command"` AND `operation.name == "/qa"`
- **And** results include session count in response
- **And** search completes in under 500ms

### Scenario 5: Search by Status and Keywords (Happy Path)
- **Given** index contains 200 feedback sessions with statuses "success", "failure", "partial"
- **When** user searches with filters: `status: "failure", keywords: ["confusing", "error", "message"]` (match any keyword)
- **Then** results include only sessions where:
  - `status == "failure"` AND
  - At least one keyword from keywords list appears in session's `keywords` array or searchable text
- **And** results display matched keyword(s) for context
- **And** search completes in under 500ms even with 1000+ sessions

### Scenario 6: Combined Filter Search (Happy Path)
- **Given** index contains 500+ feedback sessions across 6 months
- **When** user searches with combined filters:
  - `date-start: 2025-09-01`
  - `operation-type: "command"`
  - `status: "failure"`
  - `tags: ["deferral", "blocker"]`
  - `keywords: ["circular", "dependency"]`
- **Then** results include only sessions matching ALL filters:
  - Timestamp >= 2025-09-01
  - operation.type == "command"
  - status == "failure"
  - Contains at least one tag from ["deferral", "blocker"]
  - Contains at least one keyword from ["circular", "dependency"]
- **And** result count and matching criteria displayed
- **And** search completes in under 1 second

### Scenario 7: Incremental Index Update (Edge Case)
- **Given** index already contains 100 entries
- **When** a new feedback session is written
- **Then** the new entry is appended (not a full rebuild)
- **And** `last-updated` timestamp is updated to current time
- **And** existing 100 entries are unchanged
- **And** update operation completes in under 50ms

---

## Edge Cases

### Edge Case 1: Corrupted Index File Recovery
- **Given** `.devforgeai/feedback/index.json` exists but is malformed (invalid JSON, missing fields)
- **When** system attempts to write a new feedback session entry
- **Then** system detects corruption (JSON parse error)
- **And** displays error message: "Index file corrupted. Run `/feedback-reindex` to rebuild."
- **And** feedback session file IS still created (not lost due to index failure)
- **And** index write is deferred until reindex completes

### Edge Case 2: Index Reindex Command (Full Rebuild)
- **Given** index is corrupted or inconsistent with session files on disk
- **When** user runs `/feedback-reindex` command
- **Then** system:
  1. Scans all files in `.devforgeai/feedback/sessions/` directory
  2. Extracts metadata from each valid session file
  3. Rebuilds index from scratch (overwriting existing index.json)
  4. Validates all entries and formats
  5. Saves rebuilt index
  6. Displays summary: "Reindexed X sessions. Y errors found and skipped."
- **And** operation completes in under 10 seconds for 1000+ sessions

### Edge Case 3: Index Entry with Missing Optional Fields
- **Given** feedback session contains minimal data (no tags, no story-id)
- **When** entry is written to index
- **Then**:
  - `id`, `timestamp`, `operation`, `status`, `file-path` are required (HALT if missing)
  - `tags` defaults to empty array `[]` if not present
  - `story-id` defaults to `null` if not applicable
  - `keywords` defaults to empty array `[]` if extraction fails
  - Entry is still valid and searchable

### Edge Case 4: Large Index Performance (1000+ Sessions)
- **Given** index contains 1,200 feedback sessions (6+ months of data)
- **When** system performs:
  - Single filter search (date range)
  - Multi-filter search (5 combined filters)
  - Keyword search across all records
- **Then** all operations complete in under 1 second
- **And** index file size remains under 5MB

### Edge Case 5: Concurrent Index Writes
- **Given** two feedback operations complete simultaneously
- **When** both attempt to append to `.devforgeai/feedback/index.json` at the same time
- **Then**:
  - File locking or atomic append prevents data corruption
  - Both entries are successfully added (neither is lost)
  - JSON remains valid
  - `last-updated` reflects the most recent write

### Edge Case 6: Search with Special Characters and Escaping
- **Given** feedback session contains keywords with special characters:
  - "null-pointer-exception"
  - "TypeScript@4.9"
  - "error: 'database connection failed'"
- **When** user searches with keyword: "null-pointer-exception"
- **Then** results correctly match without regex escaping issues
- **And** search handles quotes, hyphens, underscores, and special characters safely

---

## Technical Specification

### API Contract: Index File Format

**File Path**: `.devforgeai/feedback/index.json`

**Index Structure**:
```json
{
  "version": "1.0",
  "last-updated": "2025-11-07T10:30:00Z",
  "feedback-sessions": [
    {
      "id": "2025-11-07T10-30-00-command-dev-success",
      "timestamp": "2025-11-07T10:30:00Z",
      "operation": {
        "type": "command",
        "name": "/dev",
        "args": "STORY-042"
      },
      "status": "success",
      "tags": ["tdd", "backend"],
      "story-id": "STORY-042",
      "keywords": ["tests passed", "refactoring", "clean code"],
      "file-path": "sessions/2025-11-07T10-30-00-command-dev-success.md"
    },
    {
      "id": "2025-11-06T14-15-00-skill-devforgeai-qa-failure",
      "timestamp": "2025-11-06T14:15:00Z",
      "operation": {
        "type": "skill",
        "name": "devforgeai-qa",
        "args": "STORY-041 deep"
      },
      "status": "failure",
      "tags": ["coverage", "deferral"],
      "story-id": "STORY-041",
      "keywords": ["circular deferral", "blocker", "invalid reason"],
      "file-path": "sessions/2025-11-06T14-15-00-skill-devforgeai-qa-failure.md"
    }
  ]
}
```

### Data Model: Index Entry

| Field | Type | Required | Validation | Description |
|-------|------|----------|-----------|-------------|
| `id` | String | Yes | Format: `[YYYY-MM-DDTHH-MM-SS]-[operation-name]-[status]` | Unique identifier, matches session filename |
| `timestamp` | String (ISO 8601) | Yes | Format: `YYYY-MM-DDTHH:MM:SSZ` | When session was created |
| `operation.type` | String | Yes | Enum: "command", "skill", "subagent" | Category of operation |
| `operation.name` | String | Yes | e.g., "/dev", "devforgeai-qa", "test-automator" | Name of operation |
| `operation.args` | String | No | e.g., "STORY-042", "deep mode" | Operation arguments |
| `status` | String | Yes | Enum: "success", "failure", "partial" | Operation outcome |
| `tags` | Array[String] | No | Lowercase strings, max 10 tags | Category tags (e.g., "deferral", "coverage", "blocker") |
| `story-id` | String \| Null | No | Format: `STORY-[0-9]+` or null | Related story if applicable |
| `keywords` | Array[String] | No | Lowercase, hyphenated if multi-word, max 10 | Searchable keywords extracted from session |
| `file-path` | String | Yes | Relative path: `sessions/[filename].md` | Location of session file |

### Search API: Filter Specification

**Search function signature**:
```
searchFeedback(filters: SearchFilters) -> SearchResults
```

**Filter Types Supported**:

```typescript
interface SearchFilters {
  dateStart?: string;           // ISO 8601 format, inclusive
  dateEnd?: string;             // ISO 8601 format, inclusive
  operationType?: string;       // "command", "skill", "subagent"
  operationName?: string;       // "/dev", "devforgeai-qa", etc.
  status?: string;              // "success", "failure", "partial"
  tags?: string[];              // Match ANY tag (OR logic)
  keywords?: string[];          // Match ANY keyword (OR logic)
  storyId?: string;             // Exact match to STORY-ID
  limit?: number;               // Max results to return (default: 100)
  offset?: number;              // Pagination offset (default: 0)
}
```

**Search Results**:
```typescript
interface SearchResults {
  total: number;                // Total matches found
  returned: number;             // Number of results returned
  filters: SearchFilters;       // Filters applied
  results: Array<{
    ...IndexEntry;
    matched-keywords?: string[];  // Keywords that matched
    matched-tags?: string[];      // Tags that matched
    preview?: string;             // First 200 chars of session content
  }>;
  executionTime: number;        // Milliseconds
}
```

### Business Rules

1. **Index Initialization**: If index file doesn't exist, create it on first feedback write (not during app startup)

2. **Incremental Updates**: Always append new entries, never rebuild entire index on each write

3. **Timestamp Format**: All timestamps stored in UTC (ISO 8601 with Z suffix), converted from local time if needed

4. **Tag Normalization**: Tags must be lowercase, hyphenated for multi-word (e.g., "circular-deferral" not "Circular Deferral")

5. **Keyword Extraction**:
   - Auto-extract 3-5 keywords from session file content
   - Prioritize: status/operation names → error messages → user actions
   - Deduplicate and normalize (lowercase, hyphenate)

6. **Search Performance**:
   - Ensure searches complete in <500ms for filters up to 1000 sessions
   - Use index for filtering, not full text scan of session files

7. **Corruption Recovery**:
   - Detect JSON parse errors when writing to index
   - Prevent data loss (write session file even if index fails)
   - Provide `/feedback-reindex` command for recovery

8. **Concurrent Access**:
   - Use atomic writes or file locking to prevent corruption during concurrent updates
   - Ensure JSON validity is maintained at all times

---

## Non-Functional Requirements

### Performance

**Search Response Time**:
- Single filter (date range, status): <200ms (for up to 1000 sessions)
- Multi-filter (3+ filters): <500ms (for up to 1000 sessions)
- Keyword search: <300ms (for up to 1000 sessions)
- Reindex operation: <10 seconds (for up to 1000 sessions)
- Incremental append: <50ms

**Index File Size**:
- ~5-10 KB per 100 sessions (approx.)
- Maximum recommended: 5 MB (supports ~500,000 sessions)

**Memory Usage**:
- Index loaded into memory: <50 MB (for 10,000 sessions)
- Search operations: No large intermediate allocations

### Reliability

**Data Integrity**:
- No data loss on concurrent writes
- Index remains valid JSON after any operation
- Failed writes don't corrupt existing data

**Recovery**:
- Reindex command rebuilds index from source files
- System detects and reports corruption
- Manual recovery path documented

**Durability**:
- All writes to index are persisted to disk
- Atomic writes prevent partial/corrupted state

### Scalability

**Session Volume**:
- Support minimum 1000 concurrent sessions without degradation
- Performance targets maintained up to 10,000 sessions

**Search Performance**:
- Response time scales logarithmically (not linearly) with session count
- Multi-filter searches maintain performance even with large datasets

### Maintainability

**Code Quality**:
- Index management logic isolated in utility module
- Search logic testable independently
- Clear separation between indexing and searching

**Documentation**:
- Index structure documented (this story)
- Search API documented with examples
- Reindex procedure documented

---

## Implementation Notes

### Phase 1: Index File Management

**Tasks**:
1. Create index file initialization logic
2. Implement append-only index writes
3. Add `last-updated` timestamp on each write
4. Validate JSON structure after each update
5. Implement corruption detection

**Files to Create/Modify**:
- Create: `.devforgeai/feedback/index.json` (on first session)
- Modify: Feedback session write path (add index append)
- Create: Index utility module (indexing functions)

### Phase 2: Search and Filtering

**Tasks**:
1. Implement search function with filter support
2. Add date range filtering
3. Add operation type/name filtering
4. Add status filtering
5. Add tag-based filtering
6. Add keyword matching
7. Implement pagination (limit/offset)
8. Optimize for performance (<500ms)

**Files to Create/Modify**:
- Modify: Index utility module (add search function)
- Create: Search result formatter
- Create: Performance benchmarks (tests)

### Phase 3: Recovery and Reindexing

**Tasks**:
1. Implement reindex command logic
2. Scan sessions directory for all files
3. Extract metadata from each session
4. Rebuild index from scratch
5. Validate output
6. Error handling and reporting
7. Progress reporting for large datasets

**Files to Create/Modify**:
- Create: `/feedback-reindex` command
- Modify: Index utility module (add rebuild function)
- Modify: Feedback session writer (detect corruption, defer writes)

### Phase 4: Testing and Documentation

**Tasks**:
1. Unit tests: Index operations (create, append, validate)
2. Unit tests: Search filters (all filter types, combinations)
3. Unit tests: Corruption scenarios
4. Integration tests: Full flow (write → index → search)
5. Performance tests: Scalability (100, 500, 1000+ sessions)
6. Concurrency tests: Simultaneous writes
7. User documentation: Search examples

**Files to Create**:
- Create: Tests for index utility module
- Create: Tests for search functionality
- Create: Integration tests
- Create: Performance benchmarks

---

## Definition of Done

- [ ] Index file initialization working (creates `.devforgeai/feedback/index.json` on first session)
- [ ] Index entries appended correctly (incremental, not rebuild)
- [ ] All required fields present in index entries
- [ ] Index file valid JSON after every operation
- [ ] Search filters implemented (date, operation, status, tags, keywords)
- [ ] Search performance meets targets (<500ms for 1000 sessions)
- [ ] Corruption detection working (detects invalid JSON, malformed entries)
- [ ] `/feedback-reindex` command implemented and tested
- [ ] Concurrent writes don't corrupt index (file locking or atomic writes)
- [ ] Pagination working (limit, offset parameters)
- [ ] All 7 acceptance criteria validated with tests
- [ ] All 6 edge cases tested and handled
- [ ] Performance tests passing (500ms, 1s, 10s targets)
- [ ] Unit test coverage >95% for indexing logic
- [ ] Integration tests covering full search workflows
- [ ] Documentation complete (API, usage examples, recovery procedures)
- [ ] Code reviewed and approved
- [ ] Deployed to staging
- [ ] QA validation passed

## Related Stories

**Depends on** (must complete first):
- STORY-013: Core Feedback Capture System (feedback session file creation)

**Blocks** (prevents these stories):
- STORY-017: Advanced Search UI (search command depends on this indexing)
- STORY-018: Feedback Analytics Dashboard (analytics depends on searchable index)

**Related**:
- STORY-014: Feedback Session Tagging (tag extraction integrated with indexing)
- STORY-015: Post-Operation Retrospective Conversation (keywords extracted from retrospectives)

---

## Questions for Clarification

1. **Keyword Extraction Strategy**: Should keywords be:
   - Auto-extracted from session content (NLP-based)?
   - Manually specified in session frontmatter?
   - Combination of both?

2. **Reindex Triggers**: Should reindex happen automatically when:
   - Corruption detected?
   - Only on manual `/feedback-reindex` command?
   - Periodically (e.g., weekly maintenance)?

3. **Search Result Limits**: Should there be:
   - Hard limit on results (e.g., max 1000)?
   - Pagination required for large result sets?
   - Aggregation/summary for >100 results?

4. **Index Versioning**: How should schema migrations be handled if index format changes in future?
   - Semantic versioning in `version` field?
   - Migration scripts?
   - Index rebuild on upgrade?

---

*To be completed during development. Developer will document: Phase completion status, implementation decisions, files created, test results, AC verification, and any refinements to requirements.*

## Implementation Status

**Phase 1**: Pending
**Phase 2**: Pending
**Phase 3**: Pending
**Phase 4**: Pending

*Detailed implementation notes will be added during development.*
